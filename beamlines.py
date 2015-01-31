import slactrac as _sltr
import logging
import numpy as np
logger=logging.getLogger(__name__)

gamma_default    = np.float_(39824)
# QS1_K1_default = np.float_(0.077225846087095e-01)
# QS2_K1_default = np.float_(02.337527121004531e-01)
QS1_K1_default   = np.float_(3.8743331090707228e-1)
QS2_K1_default   = np.float_(-2.5439067538354171e-1)
PEXT_Z           = np.float_(1994.97)
QS1_Z            = np.float_(1998.71)
AL_Z             = np.float_(2015.16)
BE_Z             = np.float_(1996.34)
ELANEX_Z         = np.float_(2015.22)
# IP2QS1_length  = np.float_(5.4217)
IP2QS1_length    = QS1_Z-PEXT_Z

def IP_to_lanex(beam_x,beam_y,
        gamma  = gamma_default,
        QS1_K1 = QS1_K1_default,
        QS2_K1 = QS2_K1_default
        ):
    logger.debug('Using lanex')
    # Beamline elements
    # IP2QS1    = _sltr.Drift(length = IP2QS1_length)
    IP2BE     = _sltr.Drift(   name= 'IP2BE'     , length = IP2QS1_length-np.float_(2.37))
    BESCATTER = _sltr.Scatter( name= 'BESCATTER' , thickness = np.float_(75e-6)            , radlength = np.float_(35.28e-2))
    BE2QS1    = _sltr.Drift(   name= 'BE2QS1'    , length = np.float_(2.37))
    QS1       = _sltr.Quad(    name= 'QS1'       , length = np.float_(5.000000000E-01)     , K1 = QS1_K1)
    LQS12QS2  = _sltr.Drift(   name= 'LQS12QS2'  , length = np.float_(4.00E+00))
    QS2       = _sltr.Quad(    name= 'QS2'       , length = np.float_(5.000000000E-01)     , K1 = QS2_K1)
    LQS22BEND = _sltr.Drift(   name= 'LQS22BEND' , length = np.float_(0.7428E+00))
    B5D36     = _sltr.Bend(    name= 'B5D36'     ,
            length = np.float_(2)*np.float_(4.889500000E-01),
            angle  = np.float_(6.0E-03),
            order  = 1,
            rotate = 90
            )
    # LBEND2ELANEX = _sltr.Drift(length = np.float_(8.792573))
    LBEND2AL  = _sltr.Drift(   name = 'LBEND2AL'  , length    = np.float_(8.792573)-np.float_(0.06))
    ALSCATTER = _sltr.Scatter( name = 'ALSCATTER' , thickness = np.float_(5e-3)                      , radlength = np.float_(8.897e-2))
    AL2ELANEX = _sltr.Drift(   name = 'AL2ELANEX' , length    = np.float_(0.06))

    beamline     = _sltr.Beamline(
            element_list=[
                # IP2QS1  ,
                IP2BE     ,
                BESCATTER ,
                BE2QS1    ,
                QS1       ,
                QS1       ,
                LQS12QS2  ,
                QS2       ,
                QS2       ,
                LQS22BEND ,
                B5D36     ,
                # LBEND2ELANEX
                LBEND2AL  ,
                ALSCATTER ,
                AL2ELANEX
                ],
            gamma  = gamma,
            beam_x = beam_x,
            beam_y = beam_y
            )
    return beamline

def IP_to_lanex_nobend(beam_x,beam_y,
        gamma  = gamma_default,
        QS1_K1 = QS1_K1_default,
        QS2_K1 = QS2_K1_default
        ):

    logger.debug('Using lanex_nobend')

    beamline = IP_to_lanex(
            beam_x = beam_x,
            beam_y = beam_y,
            gamma  = gamma,
            QS1_K1 = QS1_K1,
            QS2_K1 = QS2_K1
            )

    # Replace bend with drift
    B5D36_drift = _sltr.Drift(name='B5D36_drift',length= np.float_(2)*np.float_(4.889500000E-01))
    beamline.elements[9] = B5D36_drift

    return beamline

def IP_to_cherfar(beam_x,beam_y,
        gamma  = gamma_default,
        QS1_K1 = QS1_K1_default,
        QS2_K1 = QS2_K1_default
        ):
    logger.debug('Using cherfar')
    beamline = IP_to_lanex(beam_x,beam_y,
        gamma  = gamma,
        QS1_K1 = QS1_K1,
        QS2_K1 = QS2_K1
        )

    # print beamline.elements[12].length
    ind = 12
    logger.critical('Modifying lanex into cherfar by changing length of element: Index {}'.format(ind))
    logger.critical('Beamline elements {ind}: {value}'.format(ind=ind,value=beamline.elements[12].length))
    beamline.elements[12].length = beamline.elements[12].length + np.float_(0.8198)

    return beamline
