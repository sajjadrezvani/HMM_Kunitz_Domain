

import sys 
import numpy as np

# -------------------------------------------------------------------------
def get_preds(file_name):
    '''prende il file in input e crea una lista con e-value e classe'''
    preds=[]
    with open(file_name) as file:
        for line in file:
            v = line.rstrip().split()
            # Indici corretti per file a 3 colonne:
            # v[0] = id, v[1] = e-value, v[2] = classification (0=neg, 1=pos)
            preds.append([v[0], float(v[1]), int(v[2])])
    return preds


# -------------------------------------------------------------------------
def get_confusion_matrix(preds, threshold=0.001):
    '''
    Matrice di confusione:
         predette
            neg(0) pos(1)
    vere 
    neg(0)    TN      FP
    pos(1)    FN      TP
    '''
    cm = np.zeros((2,2))
    n = len(preds)
    
    for k in range(n):
        j = 0
        i = preds[k][2] # Classe reale (0 o 1)

        # Se l'e-value è <= soglia, la predizione è Positiva (1)
        if preds[k][1] <= threshold:
            j += 1
            
        cm[i,j] += 1

    return cm

# -------------------------------------------------------------------------
def get_accuracy(cm):
    '''ACCURACY = (TP+TN) / (TP+TN+FP+FN)'''
    return (cm[0,0] + cm[1,1]) / np.sum(cm)

def get_mcc(cm):
    '''MATTHEWS CORRELATION COEFFICIENT'''
    TP = cm[1,1]
    TN = cm[0,0]
    FP = cm[0,1]
    FN = cm[1,0]
    
    d = (TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)
    
    # Controllo di sicurezza per evitare la divisione per zero
    if d == 0:
        return 0.0
        
    return (TP*TN - FP*FN) / np.sqrt(d)

# -------------------------------------------------------------------------
if __name__=='__main__':
    file_name = sys.argv[1]
    th = float(sys.argv[2])
    
    preds = get_preds(file_name)
    cm = get_confusion_matrix(preds, th)
    acc = get_accuracy(cm)
    mcc = get_mcc(cm)
    
    # Arrotondiamo i risultati a 4 decimali per una lettura più pulita
    print(f'TH: {th}\tACC: {acc:.4f}\tMCC: {mcc:.4f}, TP:{cm[1,1]}, TN:{cm[0,0]}, FP:{cm[0,1]}, FN:{cm[1,0]}')