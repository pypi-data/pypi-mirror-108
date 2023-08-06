#  telectron - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
#
#  This file is part of telectron.
#
#  telectron is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  telectron is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with telectron.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Union, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class InputMediaInvoice(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.InputMedia`.

    Details:
        - Layer: ``128``
        - ID: ``0xf4e096c3``

    Parameters:
        title: ``str``
        description: ``str``
        invoice: :obj:`Invoice <telectron.raw.base.Invoice>`
        payload: ``bytes``
        provider: ``str``
        provider_data: :obj:`DataJSON <telectron.raw.base.DataJSON>`
        start_param: ``str``
        multiple_allowed (optional): ``bool``
        can_forward (optional): ``bool``
        photo (optional): :obj:`InputWebDocument <telectron.raw.base.InputWebDocument>`
    """

    __slots__: List[str] = ["title", "description", "invoice", "payload", "provider", "provider_data", "start_param", "multiple_allowed", "can_forward", "photo"]

    ID = 0xf4e096c3
    QUALNAME = "types.InputMediaInvoice"

    def __init__(self, *, title: str, description: str, invoice: "raw.base.Invoice", payload: bytes, provider: str, provider_data: "raw.base.DataJSON", start_param: str, multiple_allowed: Union[None, bool] = None, can_forward: Union[None, bool] = None, photo: "raw.base.InputWebDocument" = None) -> None:
        self.title = title  # string
        self.description = description  # string
        self.invoice = invoice  # Invoice
        self.payload = payload  # bytes
        self.provider = provider  # string
        self.provider_data = provider_data  # DataJSON
        self.start_param = start_param  # string
        self.multiple_allowed = multiple_allowed  # flags.1?true
        self.can_forward = can_forward  # flags.2?true
        self.photo = photo  # flags.0?InputWebDocument

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "InputMediaInvoice":
        flags = Int.read(data)
        
        multiple_allowed = True if flags & (1 << 1) else False
        can_forward = True if flags & (1 << 2) else False
        title = String.read(data)
        
        description = String.read(data)
        
        photo = TLObject.read(data) if flags & (1 << 0) else None
        
        invoice = TLObject.read(data)
        
        payload = Bytes.read(data)
        
        provider = String.read(data)
        
        provider_data = TLObject.read(data)
        
        start_param = String.read(data)
        
        return InputMediaInvoice(title=title, description=description, invoice=invoice, payload=payload, provider=provider, provider_data=provider_data, start_param=start_param, multiple_allowed=multiple_allowed, can_forward=can_forward, photo=photo)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.multiple_allowed else 0
        flags |= (1 << 2) if self.can_forward else 0
        flags |= (1 << 0) if self.photo is not None else 0
        data.write(Int(flags))
        
        data.write(String(self.title))
        
        data.write(String(self.description))
        
        if self.photo is not None:
            data.write(self.photo.write())
        
        data.write(self.invoice.write())
        
        data.write(Bytes(self.payload))
        
        data.write(String(self.provider))
        
        data.write(self.provider_data.write())
        
        data.write(String(self.start_param))
        
        return data.getvalue()
