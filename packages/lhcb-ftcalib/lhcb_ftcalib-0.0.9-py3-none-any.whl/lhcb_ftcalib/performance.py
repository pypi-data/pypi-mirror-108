import numpy as np
import pandas as pd
from uncertainties import ufloat


def p_conversion_matrix(npar):
    r""" Returns matrix :math:`C` that converts internal representation of
        parameters into the traditional form
        :math:`C\cdot (p^+_0,\cdots, p^+_n, p^-_0,\cdots,p^-_n) = (p_0,\cdots, p_n, \Delta p_0,\cdots,\Delta p_n)`

        :param npar: number of calibration parameters per flavour
        :type npar: int
        :return: parameter transformation
        :rtype: numpy.ndarray
    """
    upper = np.concatenate([0.5 * np.eye(npar), 0.5 * np.eye(npar)]).T
    lower = np.concatenate([np.eye(npar), -np.eye(npar)]).T
    return np.concatenate([upper, lower])


def tagging_rate(tagger, calibrated, selected=True):
    r""" Returns the tagging efficiency with binomial uncertainty
        :math:`\epsilon_{\mathrm{tag}}=N_t/N`

        :param stats: Tagger stats
        :type stats: TaggingData
        :param calibrated: Whether to use calibrated mistag and decisions
        :type calibrated: bool
        :param selected: Whether to only use events in selection
        :type selected: bool
        :return: Tagging efficiency
        :rtype: ufloat
    """
    if calibrated:
        assert tagger.is_calibrated()
        if selected:
            N, Nt, Neff = tagger.cstats.Nws, tagger.cstats.Nwts, tagger.cstats.Neffs
        else:
            N, Nt, Neff = tagger.cstats.Nw, tagger.cstats.Nwt, tagger.cstats.Neff
    else:
        if selected:
            N, Nt, Neff = tagger.stats.Nws, tagger.stats.Nwts, tagger.stats.Neffs
        else:
            N, Nt, Neff = tagger.stats.Nw, tagger.stats.Nwt, tagger.stats.Neff

    rate     = Nt / N
    untagged = N - Nt
    return ufloat(rate, np.sqrt(Nt * untagged / Neff) / N)


def mean_mistag(tagger, calibrated, selected=True):
    r""" Returns mean mistag of selected statistics with binomial uncertainty
        :math:`\langle\omega\rangle=N_{\mathrm{wrong}} / N`


        :param tagger: Tagger
        :type tagger: Tagger
        :param calibrated: Whether to use calibrated mistag and decisions
        :type calibrated: bool
        :param selected: Whether to use selected statistics. (Must be true)
        :type selected: bool
        :return: Mistag rate
        :rtype: ufloat
    """
    if not selected:
        return "unavailable"

    if calibrated:
        assert tagger.is_calibrated()
        Nright = np.sum(tagger.cstats.weights[tagger.cstats.correct_tags])
        Nwrong = np.sum(tagger.cstats.weights[tagger.cstats.wrong_tags])
        Nweighted = tagger.cstats.Nwts
    else:
        Nright = np.sum(tagger.stats.weights[tagger.stats.correct_tags])
        Nwrong = np.sum(tagger.stats.weights[tagger.stats.wrong_tags])
        Nweighted = tagger.stats.Nwts

    return ufloat(Nwrong / (Nwrong + Nright), np.sqrt(Nright * Nwrong / Nweighted) / Nweighted)


def tagging_power(tagger, calibrated, selected=True):
    r""" Computes the effective tagging efficiency

        :math:`\displaystyle\epsilon_{\mathrm{tag},\mathrm{eff}} = \frac{\epsilon_{\mathrm{tag}}}{\sum_{i, \mathrm{tagged}} w_i}\sum_{i, \mathrm{tagged}}w_i(1-2\eta_i)^2`

        :param tagger: Tagger
        :type tagger: Tagger
        :param calibrated: Whether to use calibrated mistag instead of raw mistag
        :type calibrated: bool
        :param selected: Whether to only use events in selection
        :type selected: bool
        :return: Tagging power
        :rtype: ufloat
    """

    tagrate = tagging_rate(tagger, calibrated, selected)

    if selected:
        if calibrated:
            assert tagger.is_calibrated()
            D = np.array(1 - 2 * tagger.cstats.eta)
            mean_D_sq = np.sum(D**2 * tagger.cstats.weights) / tagger.cstats.Nwts  # tagpower of tagged events

            # Propagate errors of mean dilution squared
            grad_calib = tagger.func.gradient(tagger.params_nominal, tagger.cstats.eta, tagger.cstats.dec, tagger.stats.avg_eta)
            grad_mean_D_sq  = -4 * np.sum(grad_calib * D * np.array(tagger.cstats.weights), axis=1) / tagger.cstats.Nwts
            mean_D_sq_err = np.sqrt(grad_mean_D_sq @ tagger.minimizer.covariance.tolist() @ grad_mean_D_sq.T)

            tagpower = tagrate * ufloat(mean_D_sq, mean_D_sq_err)
        else:
            D = 1 - 2 * tagger.stats.eta
            mean_D_sq = np.sum(D**2 * tagger.stats.weights) / tagger.stats.Nwts  # tagpower of tagged events

            tagpower = tagrate * mean_D_sq
    else:
        # Events that are only tagged are not quite as accessible, but that does not really matter
        if calibrated:
            tagged = tagger.cstats.tagged
            eta    = tagger.cstats.all_eta[tagged]
            dec    = tagger.cstats.all_dec[tagged]
            weight = tagger.cstats.all_weights[tagged]

            assert tagger.is_calibrated()
            D = np.array(1 - 2 * eta)
            mean_D_sq = np.sum(D**2 * weight) / tagger.cstats.Nwt  # tagpower of tagged events

            # Propagate errors of mean dilution squared
            grad_calib = tagger.func.gradient(tagger.params_nominal, eta, dec, tagger.stats.avg_eta)  # stats.avg_eta is correct
            grad_mean_D_sq  = -4 * np.sum(grad_calib * D * np.array(weight), axis=1) / tagger.cstats.Nwt
            mean_D_sq_err = np.sqrt(grad_mean_D_sq @ tagger.minimizer.covariance.tolist() @ grad_mean_D_sq.T)

            tagpower = tagrate * ufloat(mean_D_sq, mean_D_sq_err)
        else:
            tagged = tagger.stats.tagged
            eta    = tagger.stats.all_eta[tagged]
            dec    = tagger.stats.all_dec[tagged]
            weight = tagger.stats.all_weights[tagged]
            D = 1 - 2 * eta
            mean_D_sq = np.sum(D**2 * weight) / tagger.stats.Nwt  # tagpower of tagged events

            tagpower = tagrate * mean_D_sq
    return tagpower


def tagger_correlation(taggers, corr="dec_weight", selected=True):
    """ Compute different kinds of tagger correlations. Available correlations are

        * "fire" : Correlation of tagger decisions irrespective of decision sign
        * "dec" : Correlation of tagger decisions taking sign of decision into account
        * "dec_weight" : Correlation of tagger decisions taking sign of decision into account and weighted by tagging dilution

        :param taggers: List of taggers
        :type taggers: list
        :param corr: Type of correlation
        :type corr: string
        :param selected: Whether to only use events in selection
        :type selected: bool
        :return: Correlation matrix
        :rtype: pandas.DataFrame
    """
    if selected:
        if corr == "fire":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec[tagger.stats.selected].abs() for tagger in taggers })
        elif corr == "dec":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec[tagger.stats.selected] for tagger in taggers })
        elif corr == "dec_weight":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec[tagger.stats.selected] * (1 - 2 * tagger.stats.all_eta[tagger.stats.selected]) for tagger in taggers })
    else:
        if corr == "fire":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec.abs() for tagger in taggers })
        elif corr == "dec":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec for tagger in taggers })
        elif corr == "dec_weight":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec * (1 - 2 * tagger.stats.all_eta) for tagger in taggers })
    return decdata.corr()
