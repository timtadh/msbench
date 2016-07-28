# Author: Junqi Ma on 7/20/16

import scipy.stats as stats


def anova_f_oneway(inputs=[[]]):
    return stats.f_oneway(*inputs)
