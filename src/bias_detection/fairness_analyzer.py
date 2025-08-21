import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class ModelFairnessAnalyzer:
    """
    Bias detection and fairness analysis for educational AI models
    """
    def __init__(self, dp_threshold=0.1, eop_threshold=0.1):
        self.dp_thresh = dp_threshold
        self.eop_thresh = eop_threshold
    
    def demographic_parity(self, y_pred, sensitive_attr):
        rates = {}
        for val in np.unique(sensitive_attr):
            mask = (sensitive_attr == val)
            rates[val] = y_pred[mask].mean()
        diff = max(rates.values()) - min(rates.values())
        return rates, diff
    
    def equality_of_opportunity(self, y_true, y_pred, sensitive_attr):
        tprs = {}
        for val in np.unique(sensitive_attr):
            mask = (sensitive_attr == val)
            tp = np.sum((y_true[mask]==1) & (y_pred[mask]==1))
            fn = np.sum((y_true[mask]==1) & (y_pred[mask]==0))
            tprs[val] = tp/(tp+fn) if (tp+fn)>0 else 0
        diff = max(tprs.values()) - min(tprs.values())
        return tprs, diff
    
    def visualize(self, analysis_results, title):
        sns.barplot(x=list(analysis_results.keys()),
                    y=list(analysis_results.values()))
        plt.title(title)
        plt.ylabel('Rate')
        plt.show()
