from iep import app
from iep.application.drivers.command import SaveNewForModel

from .dbmodels import PanelData

save_new = SaveNewForModel(PanelData)
