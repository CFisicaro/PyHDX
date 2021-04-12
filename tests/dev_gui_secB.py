"""
Reload SecB and fitted data and launch  GUI

"""

from pyhdx.fileIO import read_dynamx, txt_to_np, csv_to_dataframe
from pyhdx import PeptideMasterTable
import pickle
from pyhdx.panel.apps import main_app
from pyhdx.panel.utils import reload_previous
from pyhdx.panel.base import DEFAULT_COLORS, STATIC_DIR
from pyhdx.panel.data_sources import DataSource
import panel as pn
import numpy as np
from pathlib import Path

ctrl = main_app()
directory = Path(__file__).parent
fpath_1 = directory / 'test_data' / 'ecSecB_apo.csv'
fpath_2 = directory / 'test_data' / 'ecSecB_dimer.csv'

fpaths = [fpath_1, fpath_2]
files = [p.read_bytes() for p in fpaths]

file_input = ctrl.control_panels['PeptideFileInputControl']

file_input.input_files = files
file_input.fd_state = 'Full deuteration control'
file_input.fd_exposure = 0.167

file_input.exp_state = 'SecB WT apo'
file_input.dataset_name = 'testname_123'
file_input._action_add_dataset()

file_input.exp_state = 'SecB his dimer apo'
file_input.dataset_name = 'SecB his dimer apo'  # todo catch error duplicate name
file_input._action_add_dataset()

initial_guess = ctrl.control_panels['InitialGuessControl']
initial_guess._action_fit()

fit_control = ctrl.control_panels['FitControl']
fit_control.epochs = 10

fit_control._do_fitting()


#TODO: INITIAL GUESS FOR BATCH FIT IS WRONG!õneoneon

#
#
#
#
#
# dic = {}
# dic['file_paths'] = [fpath_1, fpath_2]
# dic['norm_mode'] = 'Exp'
# dic['fd_state'] = 'Full deuteration control'
# dic['fd_exposure'] = 0.167
# dic['exp_state'] = 'SecB WT apo'
#
# # src_file = directory / 'test_data' / 'ecSecB_torch_fit.txt'
# # df = csv_to_dataframe(src_file)
# # data_dict = df.to_dict(orient='series')
# #
# #
# # data_dict['color'] = np.full_like(data_dict['r_number'], fill_value=DEFAULT_COLORS['pfact'], dtype='<U7')
# # data_source = DataSource(data_dict, x='r_number', tags=['mapping', 'pfact', 'deltaG'],
# #                          renderer='circle', size=10, name='global_fit')
# #
# # dic['sources'] = {}
# # #dic['sources']['global_fit'] = data_source  #todo: on_load!
# #
# # dic['rcsb_id'] = '1qyn'
# #
# # cluster = None
# ctrl = reload_previous(dic, ctrl)
# # ctrl.cluster = None
# #
# #
# #ctrl.control_panels['FitControl'].epochs = 10
# #ctrl.cluster = '127.0.0.1:61461'
#
#
if __name__ == '__main__':
    pn.serve(ctrl.template, show=False, static_dirs={'pyhdx': STATIC_DIR})
