from marshmallow import Schema
from marshmallow.fields import Int, Bool, Str, Nested, Float
from marshmallow.validate import OneOf


"""
API Telegram schema:
https://core.telegram.org/bots/api#update
"""


class UserSchema(Schema):
    id = Int(required=True)
    is_bot = Bool()
    first_name = Str()
    last_name = Str()
    username = Str()
    language_code = Str()


class ChatPhotoSchema(Schema):
    user = Nested(UserSchema)
    status = Str(validate=OneOf(
        choices=['creator', 'administrator', 'member', 'restricted', 'left', 'kicked']
    ))
    until_date = Int()
    can_be_edited = Bool()
    can_change_info = Bool()
    can_post_messages = Bool()
    can_edit_messages = Bool()
    can_delete_messages = Bool()
    can_invite_users = Bool()
    can_restrict_members = Bool()
    can_pin_messages = Bool()
    can_promote_members = Bool()
    can_send_messages = Bool()
    can_send_media_messages = Bool()
    can_send_other_messages = Bool()
    can_add_web_page_previews = Bool()


class ChatShame(UserSchema):
    type = Str(validate=OneOf(choices=[
        'private', 'group', 'supergroup', 'channel'
    ]))
    title = Str()
    all_members_are_administrators = Bool()
    photo = Nested(ChatPhotoSchema)
    description = Str()
    invite_link = Str()
    pinned_message = Nested('MessageSchema')
    sticker_set_name = Str()
    can_set_sticker_set = Bool()


class MessageEntityShame(Schema):
    type = Str()
    offset = Int()
    length = Int()

    url = Str()

    user = Nested(UserSchema)


class PhotoSizeSchema(Schema):
    file_id = Str()
    width = Int()
    height = Int()
    file_size = Int()


class DefaultFileSchema(Schema):
    file_id = Str()
    thumb = Nested(PhotoSizeSchema)
    file_size = Int()
    mime_type = Str()


class DefaultPhotoSizeSchema(Schema):
    width = Int()
    height = Int()


class AudioSchema(DefaultFileSchema):
    duration = Int()
    performer = Str()
    title = Str()


class DocumentSchema(DefaultFileSchema):
    file_name = Str()


class AnimationSchema(DefaultFileSchema, DefaultPhotoSizeSchema):
    duration = Int()
    file_name = Str()


class GameSchema(Schema):
    title = Str()
    description = Str()
    photo = Nested(PhotoSizeSchema, many=True)
    text = Str()
    text_entities = Nested(MessageEntityShame, many=True)
    animation = Nested(AnimationSchema)


class MaskPositionSchema(Schema):
    point = Str(validate=OneOf(
        choices=['forehead', 'eyes', 'mouth', 'chin']
    ))
    x_shift = Float()
    y_shift = Float()
    scale = Float()


class StickerSchema(DefaultPhotoSizeSchema):
    file_id = Str()
    thumb = Nested(PhotoSizeSchema)
    emoji = Str()
    set_name = Str()
    mask_position = Nested(MaskPositionSchema)
    file_size = Int()


class VideoSchema(DefaultFileSchema, DefaultPhotoSizeSchema):
    duration = Int()


class VoiceSchema(Schema):
    file_id = Str()
    duration = Int()
    mime_type = Str()
    file_size = Int()


class VideoNoteSchema(Schema):
    file_id = Str()
    length = Int()
    duration = Int()
    thumb = Nested(PhotoSizeSchema)
    file_size = Int()


class ContactSchema(Schema):
    phone_number = Str()
    first_name = Str()
    last_name = Str()
    user_id = Int()
    vcard = Str()


class LocationSchema(Schema):
    longitude = Float()
    latitude = Float()


class VenueSchema(Schema):
    location = Nested(LocationSchema)
    title = Str()
    address = Str()
    foursquare_id = Str()
    foursquare_type = Str()


class InvoiceSchema(Schema):
    title = Str()
    description = Str()
    start_parameter = Str()
    currency = Str()
    total_amount = Str()


class ShippingAddressSchema(Schema):
    country_code = Str()
    state = Str()
    city = Str()
    street_line1 = Str()
    street_line2 = Str()
    post_code = Str()


class OrderInfoSchema(Schema):
    name = Str()
    phone_number = Str()
    email = Str()
    shipping_address = Nested(ShippingAddressSchema)


class SuccessfulPaymentSchema(Schema):
    currency = Str()
    total_amount = Int()
    invoice_payload = Str()
    shipping_option_id = Str()
    order_info = Nested(OrderInfoSchema)
    telegram_payment_charge_id = Str()
    provider_payment_charge_id = Str()


class PassportFileSchema(Schema):
    file_id = Str()
    file_size = Int()
    file_date = Int()


class EncryptedPassportElementSchema(Schema):
    type = Str(validate=OneOf(choices=['personal_details', 'passport', 'driver_license', 'identity_card',
                                       'internal_passport', 'address', 'utility_bill', 'bank_statement',
                                       'rental_agreement', 'passport_registration', 'temporary_registration',
                                       'phone_number', 'email']))
    data = Str()
    phone_number = Str()
    email = Str()
    files = Nested(PassportFileSchema, many=True)
    front_side = Nested(PassportFileSchema)
    reverse_side = Nested(PassportFileSchema)
    selfie = Nested(PassportFileSchema)
    translation = Nested(PassportFileSchema, many=True)
    hash = Str()


class EncryptedCredentialsSchema(Schema):
    data = Str()
    hash = Str()
    secret = Str()


class PassportDataSchema(Schema):
    data = Nested(EncryptedPassportElementSchema, many=True)
    credentials = Nested(EncryptedCredentialsSchema)


class MessageSchema(Schema):
    class Meta:
        include = {
            'from': Nested(UserSchema, attribute="from")
        }

    message_id = Int()
    date = Int()
    chat = Nested(ChatShame)

    forward_from = Nested(UserSchema)
    forward_from_chat = Nested(ChatShame)
    forward_from_message_id = Int()
    forward_signature = Str()
    forward_date = Int()
    reply_to_message = Nested('MessageSchema')
    edit_date = Int()
    media_group_id = Str()
    author_signature = Str()
    text = Str()

    entities = Nested(MessageEntityShame, many=True)
    caption_entities = Nested(MessageEntityShame, many=True)
    audio = Nested(AudioSchema)
    document = Nested(DocumentSchema)
    animation = Nested(AnimationSchema)
    game = Nested(GameSchema)
    photo = Nested(PhotoSizeSchema, many=True)
    sticker = Nested(StickerSchema)
    video = Nested(VideoSchema)
    voice = Nested(VoiceSchema)
    video_note = Nested(VideoNoteSchema)
    caption = Str()
    contact = Nested(ContactSchema)
    location = Nested(LocationSchema)
    venue = Nested(VenueSchema)

    new_chat_members = Nested(UserSchema, many=True)
    left_chat_member = Nested(UserSchema)
    new_chat_title = Str()
    new_chat_photo = Nested(PhotoSizeSchema, many=True)
    delete_chat_photo = Bool()
    group_chat_created = Bool()
    supergroup_chat_created = Bool()
    channel_chat_created = Bool()
    migrate_to_chat_id = Int()
    migrate_from_chat_id = Int()
    pinned_message = Nested('MessageSchema')
    invoice = Nested(InvoiceSchema)
    successful_payment = Nested(SuccessfulPaymentSchema)
    connected_website = Str()
    passport_data = Nested(PassportDataSchema)


class WebHookMessageSchema(Schema):
    update_id = Int()

    message = Nested(MessageSchema)

    edited_message = Nested(MessageSchema)
    channel_post = Nested(MessageSchema)
    edited_channel_post = Nested(MessageSchema)
