from pydevmgr_elt import GROUP, UaDevice

class STYLE(GROUP):
    """ A collection of style IDs derived from GROUPs in pydevmgr + extra stuff """
    NORMAL  = "NORMAL"
    ODD     = "ODD"
    EVEN    = "EVEN"
    ERROR_TXT = "ERROR_TXT"
    OK_TXT =    "OK_TXT"
    DIFFERENT = "DIFFERENT"
    SIMILAR = "SMILAR"
    
""" Associate STYLE IDs to qt stylSheet """
qt_style_loockup = {
    STYLE.NORMAL  : "background-color: white;",
    STYLE.IDL     : "background-color: white;",
    STYLE.WARNING : "background-color: #ff9966;",
    STYLE.ERROR   : "background-color: #cc3300;",
    STYLE.OK      : "background-color: #99cc33;",
    STYLE.NOK     : "background-color: #ff9966;",
    STYLE.BUZY    : "background-color: #ffcc00;",
    STYLE.UNKNOWN : "",
    STYLE.ODD     : "background-color: #E0E0E0;",
    STYLE.EVEN    : "background-color: #F8F8F8;",
    STYLE.ERROR_TXT : "color: #cc3300;",
    STYLE.OK_TXT : "color: black;",
    STYLE.DIFFERENT : "color: #cc3300;",
    STYLE.SIMILAR: "color: black;",
}

def get_style(style):
    return qt_style_loockup.get(style, "")

""" Associate a state to a style """
state_style_loockup = {
   UaDevice.STATE.NONE  : STYLE.UNKNOWN, 
   UaDevice.STATE.OP    : STYLE.OK, 
   UaDevice.STATE.NOTOP : STYLE.NOK,
}

