# import torch
# from BrainGB.models import GAT, GCN, BrainNN
# from torch_geometric.data import Data
import numpy as np
import os
import csv

def process_data():
    # corr_data = np.loadtxt("data\\imaging\\mri_y_rsfmr_cor_gp_gp.csv", delimiter=',', dtype=str, skiprows=1)
    corr_data = np.loadtxt("data\\imaging\\mri_y_rsfmr_cor_gp_aseg.csv", delimiter=',', dtype=str, skiprows=1)
    gender_data = np.loadtxt("data\\gender-identity-sexual-health\\gish_y_gi.csv", delimiter=',', dtype=str, skiprows=1)
    subject_sex = {}
    subject_corr = {}
    for subject in gender_data:
        if subject[17] in ('1', '2'):
            subject_sex[subject[0]] = int(subject[17]) - 1
    for subject in corr_data:
        if subject[1] == "baseline_year_1_arm_1":
            if '' in subject[2:]:
                continue
            subject_corr[subject[0]] = np.array(subject[2:]).astype(float).reshape((13, 19))
    arr_sex = []
    arr_corr = []
    for subject in subject_sex:
        if subject in subject_corr:
            arr_sex.append(subject_sex[subject])
            arr_corr.append(subject_corr[subject])
    arr_sex = np.array(arr_sex)
    arr_corr = np.array(arr_corr)
    np.save("data\\subcor_data.npy", {'label': arr_sex, "corr": arr_corr})

def load_data(corr_filename, label_filename):
    corr_data = np.loadtxt(corr_filename, delimiter=',', dtype=str, skiprows=1)
    cbcl_data = np.loadtxt(label_filename, delimiter=',', dtype=str)
    return corr_data, cbcl_data

def process_data_cbcl(label_type, corr_data, label_data):
    subject_label = {}
    subject_corr = {}

    label_idx = np.where(label_data[0] == label_type)[0][0]
    print(label_idx)

    for subject in label_data[1:]:
        label_val = subject[label_idx]
        if subject[label_idx]:
            subject_label[subject[0]] = int(label_val)

    for subject in corr_data:
        if subject[1] == "baseline_year_1_arm_1":
            if '' in subject[2:]:
                continue
            subject_corr[subject[0]] = np.array(subject[2:]).astype(float).reshape((13, 19))

    arr_label = []
    arr_corr = []
    
    for subject in subject_label:
        if subject in subject_corr:
            arr_label.append(subject_label[subject])
            arr_corr.append(subject_corr[subject])

    arr_label = np.array(arr_label)
    arr_corr = np.array(arr_corr)
    np.save("data\\" + label_type, {'label': arr_label, "corr": arr_corr})


def test():
    # my_data = np.load("data\\my_data.npy", allow_pickle=True)
    # print(my_data.item()['label'].shape)
    data = np.load("data\\abide.npy", allow_pickle=True)
    print(data)
    print(len(data.item()['label']))


if __name__ == "__main__":
    # test()
    # process_data()

    corr_file = "data\\imaging\\mri_y_rsfmr_cor_gp_aseg.csv"
    label_file = "data\\mh_p_cbcl.csv"
    corr_data, label_data = load_data(corr_file, label_file)
    CBCL_SCORES_t = {"cbcl_scr_syn_anxdep_t": "Anxious/Dep.",
             "cbcl_scr_syn_withdep_t": "Depression",
             "cbcl_scr_syn_somatic_t": "Somatic",
             "cbcl_scr_syn_social_t": "Social",
             "cbcl_scr_syn_thought_t": "Thought",
             "cbcl_scr_syn_attention_t": "Attention",
             "cbcl_scr_syn_rulebreak_t": "Rule-breaking",
             "cbcl_scr_syn_aggressive_t": "Aggressive",
             "cbcl_scr_syn_internal_t": "Internalizing",
             "cbcl_scr_syn_external_t": "Externalizing"}
    for label in CBCL_SCORES_t:
        process_data_cbcl(label, corr_data, label_data)