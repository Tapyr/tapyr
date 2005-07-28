# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    PMA.Lib
#
# Purpose
#    Encapsulate classes/functions from standard Python library for use by PMA
#
# Revision Dates
#    31-Aug-2004 (CT) Creation
#     3-Sep-2004 (CT) Creation continued
#    28-Jul-2005 (CT) `encode_base64` added
#    ��revision-date�����
#--

from   _PMA                    import PMA

from   email                   import message_from_string, message_from_file
from   email.Encoders          import encode_base64
from   email.Generator         import *
from   email.Header            import *
from   email.Message           import *
from   email.MIMEAudio         import MIMEAudio
from   email.MIMEBase          import MIMEBase
from   email.MIMEImage         import MIMEImage
from   email.MIMEMessage       import MIMEMessage
from   email.MIMEMultipart     import MIMEMultipart
from   email.MIMENonMultipart  import MIMENonMultipart
from   email.MIMEText          import MIMEText
from   email.Parser            import *
from   email.Utils             import *

import mailbox
import mailcap

if __name__ != "__main__" :
    PMA._Export_Module ()
### __END__ PMA.Lib
