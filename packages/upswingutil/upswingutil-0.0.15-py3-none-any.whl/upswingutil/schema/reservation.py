from typing import Optional
from typing import List
from upswingutil.schema import Token
from pydantic import BaseModel


class PropertyInfo(BaseModel):
    hotelId: str
    clientId: str
    orgId: str
    agent: str
    hotelName: str
    numberOfRooms: int
    roomId: str
    roomName: str
    roomType: str
    roomClass: str
    roomTypeCharged: str
    roomNumberLocked: bool
    pseudoRoom: bool


class TravelType(BaseModel):
    id: int
    name: str
    type: str
    score: float
    addedBy: str


class GuestProfile(BaseModel):
    guestId: str
    firstName: str
    middleName: Optional[str] = ''
    lastName: str
    language: Optional[str] = ''


class GuestInfo(BaseModel):
    adultCount: int
    childrenCount: int
    infantCount: int
    guest_list: List[GuestProfile]


class BookingChannelInfo(BaseModel):
    saleSourceType: str
    saleSourceCode: str
    sourceCode: str
    sourceDescription: str
    channelCode: str


class BookingFinancialInfo(BaseModel):
    currencyCode: str
    rateAmount: float
    paymentMethod: str

    fixedRate: Optional[bool]
    rateSuppressed: Optional[bool]
    ratePlanCode: Optional[str]


class Reservation(BaseModel):
    class ReservationIdObj(BaseModel):
        id: str
        name: str

    class OriginalTimeStamp(BaseModel):
        startDate: str
        endDate: str

    class ExpectedTimes(BaseModel):
        expectedArrivalTime: Optional[str] = ''
        expectedDepartureTime: Optional[str] = ''

    resvId: str
    token: Optional[Token]
    reservationIdObj: Optional[dict]
    arrivalDate: str
    departureDate: str
    durationInSeconds: int
    confirmationDate: Optional[str] = ''
    createdDate: Optional[str] = ''
    cancelledDate: Optional[str] = ''
    modifiedDate: Optional[str] = ''
    preAuthExpDate: Optional[str] = ''
    originalTimeStamp: OriginalTimeStamp
    propertyInfo: PropertyInfo
    reservationStatus: str
    advanceCheckIn: Optional[dict]
    expectedTimes: Optional[ExpectedTimes]
    travel_type: Optional[List[TravelType]] = []
    guestInfo: Optional[GuestInfo]
    channelInfo: BookingChannelInfo
    financialInfo: BookingFinancialInfo
    allowMobileCheckout: Optional[bool] = True
    optedForCommunication: Optional[bool] = True


if __name__ == '__main__':
    reservation = Reservation(
        resvId="001",
        agent="ORACLE",
        arrivalDate="2021-01-01",
        departureDate="2021-01-10",
        reservationStatus='NoShow',
        propertyInfo={
            'hotelId': 'SAN01',
            'orgId': 'OHILP',
            'clientId': 'SAN01',
            'agent': 'ORACLE',
            'hotelName': 'OHIP Sandbox 1',
            'numberOfRooms': 1,
            'roomId': '001',
            'roomName': '001',
            'roomType': 'DBL',
            'roomClass': 'STD',
            'roomTypeCharged': 'DBL',
            'roomNumberLocked': False,
            'pseudoRoom':  False
        },
        travel_type=[
            {
                'id': 1,
                'name': 'Business',
                'score': 1,
                'addedBy': 'ALVIE'
            }
        ],
        originalTimeStamp={
            'startDate': '2021-01-21',
            'endDate': '2021-01-31'
        },
        channelInfo={
            'bookingSourceType': '',
            'bookingSourceCode': '',
            'bookingChannelCode': ''
        },
        financialInfo={
            'currencyCode': 'USD',
            'rateAmount': 200,
            'paymentMethod': 'CA',
            'fixedRate': True,
            'rateSuppressed': False,
            'ratePlanCode': 'SDF'
        },
        guestInfo={
            'adultCount': 1,
            'childrenCount': 1,
            'infantCount': 1,
            'guest_list': [
                {
                    'guestId': '0002123',
                    'firstName': 'Harsh',
                    'lastName': 'Mathur',
                    'language': 'E',
                }
            ]
        }
    )
    print(reservation.json())
