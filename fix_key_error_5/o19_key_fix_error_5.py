#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2021 https://github.com/Oops19
#

from fix_key_error_5.modinfo import ModInfo
from sims.aging.aging_tuning import AgingTuning
from sims.sim_info_types import Species
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_teardown import S4CLZoneTeardownEvent
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

from sims.aging.aging_mixin import AgingMixin

log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().author}_{ModInfo.get_identity().name}", ModInfo.get_identity().name)
log.enable()
log.warn("This mod injects into AgingMixin.get_aging_data() and tries to catch tuning errors.")
log.warn("It has been build for v1.80.69 and may be outdated by now.")

error_data = {}


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), AgingMixin, AgingMixin.get_aging_data.__name__, handle_exceptions=False)
def o19_get_aging_data(original, self):
    try:
        aging_data =  original(self)
    except Exception as e:
        aging_data = AgingTuning.AGING_DATA[Species.HUMAN]

        global error_data
        error_text = f"{e}"
        error_count = error_data.get(error_text, 0)
        if error_count == 0:
            log.debug(f"Replacing {self.species} with Species.HUMAN. Error '{error_text}' occurred.")
        error_count += 1
        error_data.update({error_text: error_count})
    return aging_data


@CommonEventRegistry.handle_events(ModInfo.get_identity().name)
def handle_event(event_data: S4CLZoneTeardownEvent):
    global error_data
    for error_text, error_count in error_data.items():
        log.warn(f"Error '{error_text}' repeated {error_count} times.")
    error_data = {}


log.info("Fallback to HUMAN for get_aging_data() added.")
