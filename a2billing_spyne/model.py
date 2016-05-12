# encoding: utf8
#
# This file is part of the a2billing-spyne project.
# Copyright (c), Arskom Ltd. (arskom.com.tr),
#                Cemrecan Ünal <unalcmre@gmail.com>.
#                Burak Arslan <burak.arslan@arskom.com.tr>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the Arskom Ltd. nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


from datetime import date

from spyne import table, Unicode, Date, Integer32, Float, Integer64, Decimal, Time

from neurons.model import TableModel


class CardGroup(TableModel):
    __tablename__ = 'cc_card_group'

    name = Unicode(1, )
    description = Unicode(null=True)
    users_perms = Integer32(default=0)
    id_agent = Integer32(default=0)


class Card(TableModel):
    __tablename__ = "cc_card"

    # user = ForeignKeyField(User, related_name='tweets')
    creationdate = Date(default_factory=date.now)
    firstusedate = Unicode(1, null=True)
    expirationdate = Unicode(1, null=True)
    enableexpire = Unicode(1, null=True)
    expiredays = Unicode(1, null=True)
    username = Unicode(1, null=False)
    useralias = Unicode(1, )
    uipass = Unicode(1, )
    credit = Float(default=0.0)
    tariff = Unicode(1, )
    id_didgroup = Unicode(1, null=True)
    activated = Unicode(1, choices=(('f', 'False'), ('t', 'True')))
    status = Integer32(default=1)
    lastname = Unicode(1, default='')
    firstname = Unicode(1, default='')
    address = Unicode(1, default='')
    city = Unicode(1, default='')
    state = Unicode(1, default='')
    country = Unicode(1, default='')
    zipcode = Unicode(1, default='')
    phone = Unicode(1, default='')
    email = Unicode(1, default='')
    fax = Unicode(1, default='')
    # inuse = Unicode(1, null=True)
    simultaccess = Integer32(default=0)
    currency = Unicode(1, default='USD')
    # lastuse = Unicode(1, null=True)
    # nbused = Unicode(1, null=True)
    typepaid = Integer32(default=0)
    creditlimit = Integer32(default=0)
    voipcall = Integer32(default=0)
    sip_buddy = Integer32(default=0)
    iax_buddy = Integer32(default=0)
    language = Unicode(1, default='en')
    redial = Unicode(1, default='')
    runservice = Unicode(1, null=True)
    # nbservice = Unicode(1, null=True)
    # id_campaign = Unicode(1, null=True)
    # num_trials_done = Unicode(1, null=True)
    vat = Float(null=False, default=0)
    # servicelastrun = Unicode(1, null=True)
    # Using Decimal produce an error
    initialbalance = Float(default=0.0)
    invoiceday = Integer32(default=1)
    autorefill = Integer32(default=0)
    loginkey = Unicode(1, default='')
    mac_addr = Unicode(1, default='00-00-00-00-00-00')
    id_timezone = Integer32(default=0)
    tag = Unicode(1, default='')
    voicemail_permitted = Integer32(default=0)
    voicemail_activated = Integer32(default=0)
    # last_notification = Unicode(1, null=True)
    email_notification = Unicode(1, default='')
    notify_email = Integer32(default=0)
    credit_notification = Integer32(default=-1)
    id_group = Integer32(default=1)
    company_name = Unicode(1, default='')
    company_website = Unicode(1, default='')
    vat_rn = Unicode(1, null=True)
    traffic = Integer64(default=0)
    traffic_target = Unicode(1, default='')
    # Using Decimal produce an error
    discount = Float(default=0.0)
    # restriction = Unicode(1, null=True)
    # id_seria = Unicode(1, null=True)
    # serial = Unicode(1, null=True)
    block = Integer32(default=0)
    lock_pin = Unicode(1, null=True)
    lock_date = Date(null=True)
    max_concurrent = Integer32(default=10)
    # is_published = BooleanField(default=True)



class Callerid(TableModel):
    __tablename__ = 'cc_callerid'

    # id = Integer64(primary_key=True)
    # id_cc_card = Integer64()
    id_cc_card = Card.store_as(table(left='id_cc_card'))
    activated = Unicode(1, default='t')
    cid = Unicode(1, unique=True)


class Logrefill(TableModel):
    __tablename__ = 'cc_logrefill'

    # id = Integer64(primary_key=True)
    # card = ForeignKeyField(Card, db_column='card_id')
    card = Integer64(db_column='card_id', null=True)
    date = Date(null=True)
    agent = Integer64(db_column='agent_id', null=True)
    credit = Decimal(default=0.0)
    description = Unicode(null=True)
    # refill_type (amount:0, correction:1, extra fee:2,agent refund:3)
    refill_type = Integer32(default=0)
    added_invoice = Integer32(default=0)


class Logpayment(TableModel):
    __tablename__ = 'cc_logpayment'

    card = Integer64(db_column='card_id')
    date = Date(null=True, default_factory=date.now)
    description = Unicode(null=True)
    payment = Decimal(default=0.0)
    # payment_type (amount:0, correction:1, extra fee:2,agent refund:3)
    payment_type = Integer32(default=0)
    id_logrefill = Integer64(null=True)
    added_commission = Integer32(default=0)
    added_refill = Integer32(default=0)
    agent = Integer64(db_column='agent_id', null=True)


class Country(TableModel):
    __tablename__ = 'cc_country'

    # id = Integer64(primary_key=True)
    countrycode = Unicode(1, )
    countryname = Unicode(1, )
    countryprefix = Unicode(1, )



class Did(TableModel):
    __tablename__ = 'cc_did'

    # id = Integer64(primary_key=True)
    # id_cc_country = Integer32()
    # id_cc_didgroup = Integer64()
    id_cc_didgroup = Integer32(null=False)
    id_cc_country = Country.store_as(table(left='id_cc_country'))
    activated = Integer32(null=False)
    did = Unicode(1, unique=True)
    reserved = Integer32(null=True)
    iduser = Integer64(null=False)
    creationdate = Date(default_factory=date.now)
    startingdate = Date()
    expirationdate = Date()
    aleg_carrier_connect_charge = Decimal()
    aleg_carrier_connect_charge_offp = Decimal()
    aleg_carrier_cost_min = Decimal()
    aleg_carrier_cost_min_offp = Decimal()
    aleg_carrier_increment = Integer32()
    aleg_carrier_increment_offp = Integer32()
    aleg_carrier_initblock = Integer32()
    aleg_carrier_initblock_offp = Integer32()
    aleg_retail_connect_charge = Decimal()
    aleg_retail_connect_charge_offp = Decimal()
    aleg_retail_cost_min = Decimal()
    aleg_retail_cost_min_offp = Decimal()
    aleg_retail_increment = Integer32()
    aleg_retail_increment_offp = Integer32()
    aleg_retail_initblock = Integer32()
    aleg_retail_initblock_offp = Integer32()
    aleg_timeinterval = Unicode(null=True)
    billingtype = Integer32(null=True)
    connection_charge = Decimal()
    description = Unicode(null=True)
    fixrate = Float()
    max_concurrent = Integer32()
    secondusedreal = Integer32(null=True)
    selling_rate = Decimal()

class DidDestination(TableModel):
    __tablename__ = 'cc_did_destination'

    # id = Integer64(primary_key=True)
    destination = Unicode(1, null=True)
    priority = Integer32()
    id_cc_card = Integer64()
    id_cc_did = Integer64()
    activated = Integer32()
    secondusedreal = Integer32(null=True)
    voip_call = Integer32(null=True)
    validated = Integer32(null=True)
    # creationdate = Date()


class Call(TableModel):
    __tablename__ = 'cc_call'

    # id = Integer64(primary_key=True)
    sessionid = Unicode(1, default=0)
    uniqueid = Unicode(1, null=False)
    card_id = Integer64(null=False, db_column='card_id')
    nasipaddress = Unicode(1, null=False)
    starttime = Date(index=True, default_factory=date.now)
    stoptime = Unicode(1, default="0000-00-00 00:00:00")
    buycost = Decimal(null=True)
    calledstation = Unicode(1, index=True)
    destination = Integer32(null=True)
    dnid = Unicode(1, null=False)
    id_card_package_offer = Integer32(null=True)
    id_did = Integer32(null=True)
    id_ratecard = Integer32(null=True)
    id_tariffgroup = Integer32(null=True)
    id_tariffplan = Integer32(null=True)
    id_trunk = Integer32(null=True)
    real_sessiontime = Integer32(null=True)
    sessionbill = Float(null=True)
    sessiontime = Integer32(null=True)
    sipiax = Integer32(null=True)
    src = Unicode(1, )
    terminatecauseid = Integer32(index=True, null=True)

class Charge(TableModel):
    __tablename__ = 'cc_charge'

    # id = Integer64(primary_key=True)
    amount = Float(default=0)
    charged_status = Integer32(default=0)
    # Values: 1:charge DID setup, 2:Montly charge for DID use, 3:Subscription fee, 4:Extra Charge
    chargetype = Integer32(null=True, default=4)
    cover_from = Date(null=True)
    cover_to = Date(null=True)
    creationdate = Date(index=True, default_factory=date.now)
    description = Unicode(null=True)
    id_cc_card = Card(db_column='id_cc_card')
    id_cc_card_subscription = Integer64(null=True)
    # id_cc_did = Integer64(null=True)
    id_cc_did = Did.store_as(table(left='id_cc_did', default=0))
    iduser = Integer32(default=0)
    invoiced_status = Integer32(default=0)

#
# Previous Models are currently used
#


class Agent(TableModel):

    __tablename__ = 'cc_agent'

    active = Unicode(1, )
    address = Unicode(1, null=True)
    bank_info = Unicode(null=True)
    banner = Unicode(null=True)
    city = Unicode(1, null=True)
    com_balance = Decimal()
    commission = Decimal()
    company = Unicode(1, null=True)
    country = Unicode(1, null=True)
    credit = Decimal()
    currency = Unicode(1, null=True)
    datecreation = Date()
    email = Unicode(1, null=True)
    fax = Unicode(1, null=True)
    firstname = Unicode(1, null=True)
    id = Integer64(primary_key=True)
    id_tariffgroup = Integer32(null=True)
    language = Unicode(1, null=True)
    lastname = Unicode(1, null=True)
    locale = Unicode(1, null=True)
    location = Unicode(null=True)
    login = Unicode(1, unique=True)
    options = Integer32()
    passwd = Unicode(1, null=True)
    perms = Integer32(null=True)
    phone = Unicode(1, null=True)
    state = Unicode(1, null=True)
    threshold_remittance = Decimal()
    vat = Decimal()
    zipcode = Unicode(1, null=True)


class AgentCommission(TableModel):
    __tablename__ = 'cc_agent_commission'

    amount = Decimal()
    commission_percent = Decimal()
    commission_type = Integer32()
    date = Date()
    description = Unicode(null=True)
    id = Integer64(primary_key=True)
    id_agent = Integer32()
    id_card = Integer64()
    id_payment = Integer64(null=True)

class AgentSignup(TableModel):
    __tablename__ = 'cc_agent_signup'

    code = Unicode(1, unique=True)
    id = Integer64(primary_key=True)
    id_agent = Integer32()
    id_group = Integer32()
    id_tariffgroup = Integer32()


class AgentTariffgroup(TableModel):
    __tablename__ = 'cc_agent_tariffgroup'

    id_agent = Integer64()
    id_tariffgroup = Integer32()



class Alarm(TableModel):

    __tablename__ = 'cc_alarm'

    datecreate = Date()
    datelastrun = Date()
    emailreport = Unicode(1, null=True)
    id = Integer64(primary_key=True)
    id_trunk = Integer32(null=True)
    maxvalue = Float()
    minvalue = Float()
    name = Unicode()
    numberofalarm = Integer32()
    numberofrun = Integer32()
    periode = Integer32()
    status = Integer32()
    type = Integer32()

class AlarmReport(TableModel):
    __tablename__ = 'cc_alarm_report'

    calculatedvalue = Float()
    cc_alarm = Integer64(db_column='cc_alarm_id')
    daterun = Date()
    id = Integer64(primary_key=True)


class AutorefillReport(TableModel):
    __tablename__ = 'cc_autorefill_report'

    daterun = Date()
    id = Integer64(primary_key=True)
    totalcardperform = Integer32(null=True)
    totalcredit = Decimal(null=True)


class Backup(TableModel):
    __tablename__ = 'cc_backup'

    creationdate = Date()
    id = Integer64(primary_key=True)
    name = Unicode(1, unique=True)
    path = Unicode(1, )


class BillingCustomer(TableModel):
    __tablename__ = 'cc_billing_customer'

    date = Date()
    id = Integer64(primary_key=True)
    id_card = Integer64()
    id_invoice = Integer64()
    start_date = Date(null=True)


class CallArchive(TableModel):
    __tablename__ = 'cc_call_archive'

    buycost = Decimal(null=True)
    calledstation = Unicode(1, index=True)
    card = Integer64(db_column='card_id')
    destination = Integer32(null=True)
    dnid = Unicode(1, )
    id = Integer64(primary_key=True)
    id_card_package_offer = Integer32(null=True)
    id_did = Integer32(null=True)
    id_ratecard = Integer32(null=True)
    id_tariffgroup = Integer32(null=True)
    id_tariffplan = Integer32(null=True)
    id_trunk = Integer32(null=True)
    nasipaddress = Unicode(1, )
    real_sessiontime = Integer32(null=True)
    sessionbill = Float(null=True)
    sessionid = Unicode(1, )
    sessiontime = Integer32(null=True)
    sipiax = Integer32(null=True)
    src = Unicode(1, )
    starttime = Date(index=True)
    stoptime = Date()
    terminatecauseid = Integer32(index=True, null=True)
    uniqueid = Unicode(1, )


class CallbackSpool(TableModel):
    __tablename__ = 'cc_callback_spool'

    account = Unicode(1, null=True)
    actionid = Unicode(1, null=True)
    agi_result = Unicode(1, null=True)
    application = Unicode(1, null=True)
    async = Unicode(1, null=True)
    callback_time = Date()
    callerid = Unicode(1, null=True)
    channel = Unicode(1, null=True)
    context = Unicode(1, null=True)
    data = Unicode(1, null=True)
    entry_time = Date()
    exten = Unicode(1, null=True)
    id = Integer64(primary_key=True)
    id_server = Integer32(null=True)
    id_server_group = Integer32(null=True)
    last_attempt_time = Date()
    manager_result = Unicode(1, null=True)
    num_attempt = Integer32()
    priority = Unicode(1, null=True)
    server_ip = Unicode(1, null=True)
    status = Unicode(1, null=True)
    timeout = Unicode(1, null=True)
    uniqueid = Unicode(1, null=True, unique=True)
    variable = Unicode(1, null=True)

class CallplanLcr(TableModel):
    __tablename__ = 'cc_callplan_lcr'

    buyrate = Decimal(null=True)
    connectcharge = Decimal(null=True)
    destination = Unicode(1, null=True)
    dialprefix = Unicode(1, null=True)
    id = Integer32(null=True)
    id_trunk = Integer32(null=True)
    idtariffplan = Integer32(null=True)
    initblock = Integer32(null=True)
    ratecard = Integer32(db_column='ratecard_id', null=True)
    rateinitial = Decimal(null=True)
    startdate = Date(null=True)
    stopdate = Date(null=True)
    tariffgroup = Integer32(db_column='tariffgroup_id', null=True)


class Campaign(TableModel):
    __tablename__ = 'cc_campaign'

    creationdate = Date()
    daily_start_time = Time()
    daily_stop_time = Time()
    description = Unicode(null=True)
    expirationdate = Date()
    forward_number = Unicode(1, null=True)
    frequency = Integer32()
    friday = Integer32()
    id_campaign_config = Integer32()
    id_card = Integer64()
    id_cid_group = Integer32()
    monday = Integer32()
    name = Unicode(1, unique=True)
    nb_callmade = Integer32(null=True)
    saturday = Integer32()
    secondusedreal = Integer32(null=True)
    startingdate = Date()
    status = Integer32()
    sunday = Integer32()
    thursday = Integer32()
    tuesday = Integer32()
    wednesday = Integer32()


class CampaignConfig(TableModel):
    __tablename__ = 'cc_campaign_config'

    context = Unicode(1, )
    description = Unicode(null=True)
    flatrate = Decimal()
    name = Unicode(1, )

class CampaignPhonebook(TableModel):
    __tablename__ = 'cc_campaign_phonebook'

    id_campaign = Integer32()
    id_phonebook = Integer32()


class CampaignPhonestatus(TableModel):
    __tablename__ = 'cc_campaign_phonestatus'

    id_callback = Unicode(1, )
    id_campaign = Integer32()
    id_phonenumber = Integer64()
    lastuse = Date()
    status = Integer32()



class CampaignconfCardgroup(TableModel):
    __tablename__ = 'cc_campaignconf_cardgroup'

    id_campaign_config = Integer32()
    id_card_group = Integer32()




class CardArchive(TableModel):
    __tablename__ = 'cc_card_archive'

    vat_rn = Unicode(1, db_column='VAT_RN', null=True)
    activated = Unicode(1, )
    activatedbyuser = Unicode(1, )
    address = Unicode(1, null=True)
    autorefill = Integer32(null=True)
    city = Unicode(1, null=True)
    company_name = Unicode(1, null=True)
    company_website = Unicode(1, null=True)
    country = Unicode(1, null=True)
    creationdate = Date(index=True)
    credit = Decimal()
    credit_notification = Integer32()
    creditlimit = Integer32(null=True)
    currency = Unicode(1, null=True)
    discount = Decimal()
    email = Unicode(1, null=True)
    email_notification = Unicode(1, null=True)
    enableexpire = Integer32(null=True)
    expirationdate = Date()
    expiredays = Integer32(null=True)
    fax = Unicode(1, null=True)
    firstname = Unicode(1, null=True)
    firstusedate = Date()
    iax_buddy = Integer32(null=True)
    id = Integer64(primary_key=True)
    id_campaign = Integer32(null=True)
    id_didgroup = Integer32(null=True)
    id_group = Integer32()
    id_timezone = Integer32(null=True)
    initialbalance = Decimal()
    inuse = Integer32(null=True)
    invoiceday = Integer32(null=True)
    language = Unicode(1, null=True)
    last_notification = Date(null=True)
    lastname = Unicode(1, null=True)
    lastuse = Date()
    loginkey = Unicode(1, null=True)
    mac_addr = Unicode(1, )
    nbservice = Integer32(null=True)
    nbused = Integer32(null=True)
    notify_email = Integer32()
    num_trials_done = Integer64(null=True)
    phone = Unicode(1, null=True)
    redial = Unicode(1, null=True)
    restriction = Integer32()
    runservice = Integer32(null=True)
    servicelastrun = Date()
    simultaccess = Integer32(null=True)
    sip_buddy = Integer32(null=True)
    state = Unicode(1, null=True)
    status = Integer32(null=True)
    tag = Unicode(1, null=True)
    tariff = Integer32(null=True)
    traffic = Integer64(null=True)
    traffic_target = Unicode(null=True)
    typepaid = Integer32(null=True)
    uipass = Unicode(1, null=True)
    useralias = Unicode(1, )
    username = Unicode(1, index=True)
    vat = Float()
    voicemail_activated = Integer32()
    voicemail_permitted = Integer32()
    voipcall = Integer32(null=True)
    zipcode = Unicode(1, null=True)


class CardHistory(TableModel):
    __tablename__ = 'cc_card_history'

    datecreated = Date()
    description = Unicode(null=True)
    id = Integer64(primary_key=True)
    id_cc_card = Integer64(null=True)


class CardPackageOffer(TableModel):
    __tablename__ = 'cc_card_package_offer'

    date_consumption = Date(index=True)
    id = Integer64(primary_key=True)
    id_cc_card = Integer64(index=True)
    id_cc_package_offer = Integer64(index=True)
    used_secondes = Integer64()


class CardSeria(TableModel):
    __tablename__ = 'cc_card_seria'

    description = Unicode(null=True)
    name = Unicode(1, )
    value = Integer64()


class CardSubscription(TableModel):
    __tablename__ = 'cc_card_subscription'

    id = Integer64(primary_key=True)
    id_cc_card = Integer64(null=True)
    id_subscription_fee = Integer32(null=True)
    last_run = Date()
    limit_pay_date = Date()
    next_billing_date = Date()
    paid_status = Integer32()
    product = Unicode(1, db_column='product_id', null=True)
    product_name = Unicode(1, null=True)
    startdate = Date()
    stopdate = Date()


class CardgroupService(TableModel):
    __tablename__ = 'cc_cardgroup_service'

    id_card_group = Integer32()
    id_service = Integer32()



class Config(TableModel):
    __tablename__ = 'cc_config'

    config_description = Unicode(1, null=True)
    config_group_title = Unicode(1, )
    config_key = Unicode(1, null=True)
    config_listvalues = Unicode(1, null=True)
    config_title = Unicode(1, null=True)
    config_value = Unicode(1, null=True)
    config_valuetype = Integer32()


class ConfigGroup(TableModel):
    __tablename__ = 'cc_config_group'

    group_description = Unicode(1, )
    group_title = Unicode(1, unique=True)


class Configuration(TableModel):
    __tablename__ = 'cc_configuration'

    configuration_description = Unicode(1, )
    configuration = Integer32(primary_key=True, db_column='configuration_id')
    configuration_key = Unicode(1, )
    configuration_title = Unicode(1, )
    configuration_type = Integer32()
    configuration_value = Unicode(1, )
    set_function = Unicode(1, null=True)
    use_function = Unicode(1, null=True)

class Currencies(TableModel):
    __tablename__ = 'cc_currencies'

    basecurrency = Unicode(1, )
    currency = Unicode(1, unique=True)
    lastupdate = Date()
    name = Unicode(1, )
    value = Decimal()


class DidUse(TableModel):
    __tablename__ = 'cc_did_use'

    activated = Integer32(null=True)
    id = Integer64(primary_key=True)
    id_cc_card = Integer64(null=True)
    id_did = Integer64()
    month_payed = Integer32(null=True)
    releasedate = Date()
    reminded = Integer32()
    reservationdate = Date()


class Didgroup(TableModel):
    __tablename__ = 'cc_didgroup'

    creationdate = Date()
    didgroupname = Unicode(1, )
    id = Integer64(primary_key=True)


class EpaymentLog(TableModel):
    __tablename__ = 'cc_epayment_log'

    amount = Unicode(1, )
    cardid = Integer64()
    cc_expires = Unicode(1, null=True)
    cc_number = Unicode(1, null=True)
    cc_owner = Unicode(1, null=True)
    creationdate = Date()
    credit_card_type = Unicode(1, null=True)
    currency = Unicode(1, null=True)
    cvv = Unicode(1, null=True)
    id = Integer64(primary_key=True)
    item = Integer64(db_column='item_id', null=True)
    item_type = Unicode(1, null=True)
    paymentmethod = Unicode(1, )
    status = Integer32()
    transaction_detail = Unicode(null=True)
    vat = Float()


class EpaymentLogAgent(TableModel):
    __tablename__ = 'cc_epayment_log_agent'

    agent = Integer64(db_column='agent_id')
    amount = Unicode(1, )
    cc_expires = Unicode(1, null=True)
    cc_number = Unicode(1, null=True)
    cc_owner = Unicode(1, null=True)
    creationdate = Date()
    credit_card_type = Unicode(1, null=True)
    currency = Unicode(1, null=True)
    cvv = Unicode(1, null=True)
    id = Integer64(primary_key=True)
    paymentmethod = Unicode(1, )
    status = Integer32()
    transaction_detail = Unicode(null=True)
    vat = Float()


class IaxBuddies(TableModel):
    __tablename__ = 'cc_iax_buddies'

    defaultip = Unicode(1, db_column='DEFAULTip', null=True)
    accountcode = Unicode(1, )
    adsi = Unicode(1, )
    allow = Unicode(1, )
    amaflags = Unicode(1, null=True)
    auth = Unicode(1, )
    callerid = Unicode(1, )
    cid_number = Unicode(1, )
    codecpriority = Unicode(1, )
    context = Unicode(1, )
    dbsecret = Unicode(1, )
    deny = Unicode(1, )
    disallow = Unicode(1, )
    encryption = Unicode(1, )
    forcejitterbuffer = Unicode(1, )
    fullname = Unicode(1, )
    host = Unicode(1, index=True)
    id_cc_card = Integer32()
    inkeys = Unicode(1, )
    ipaddr = Unicode(1, index=True)
    jitterbuffer = Unicode(1, )
    language = Unicode(1, null=True)
    mask = Unicode(1, )
    maxauthreq = Unicode(1, )
    maxcallnumbers = Unicode(1, )
    maxcallnumbers_nonvalidated = Unicode(1, )
    mohinterpret = Unicode(1, )
    mohsuggest = Unicode(1, )
    name = Unicode(1, unique=True)
    outkey = Unicode(1, )
    permit = Unicode(1, null=True)
    port = Unicode(1, index=True)
    qualify = Unicode(1, null=True)
    qualifyfreqnotok = Unicode(1, )
    qualifyfreqok = Unicode(1, )
    qualifysmoothing = Unicode(1, )
    regcontext = Unicode(1, )
    regexten = Unicode(1, )
    regseconds = Integer32()
    requirecalltoken = Unicode(1, )
    secret = Unicode(1, )
    sendani = Unicode(1, )
    setvar = Unicode(1, )
    sourceaddress = Unicode(1, )
    timezone = Unicode(1, )
    transfer = Unicode(1, )
    trunk = Unicode(1, null=True)
    type = Unicode(1, )
    username = Unicode(1, )


class Invoice(TableModel):
    __tablename__ = 'cc_invoice'

    date = Date()
    description = Unicode()
    id = Integer64(primary_key=True)
    id_card = Integer64()
    paid_status = Integer32()
    reference = Unicode(1, null=True, unique=True)
    status = Integer32()
    title = Unicode(1, )

class InvoiceConf(TableModel):
    __tablename__ = 'cc_invoice_conf'

    key_val = Unicode(1, unique=True)
    value = Unicode(1, )



class InvoiceItem(TableModel):
    __tablename__ = 'cc_invoice_item'

    vat = Decimal(db_column='VAT')
    date = Date()
    description = Unicode()
    id = Integer64(primary_key=True)
    id_ext = Integer64(null=True)
    id_invoice = Integer64()
    price = Decimal()
    type_ext = Unicode(1, null=True)


class InvoicePayment(TableModel):
    __tablename__ = 'cc_invoice_payment'

    id_invoice = Integer64()
    id_payment = Integer64()



class Iso639(TableModel):
    __tablename__ = 'cc_iso639'

    charset = Unicode(1, )
    code = Unicode(1, primary_key=True)
    lname = Unicode(1, null=True)
    name = Unicode(1, unique=True)

class LogpaymentAgent(TableModel):
    __tablename__ = 'cc_logpayment_agent'

    added_refill = Integer32()
    agent = Integer64(db_column='agent_id')
    date = Date()
    description = Unicode(null=True)
    id = Integer64(primary_key=True)
    id_logrefill = Integer64(null=True)
    payment = Decimal()
    payment_type = Integer32()

class LogrefillAgent(TableModel):
    __tablename__ = 'cc_logrefill_agent'

    agent = Integer64(db_column='agent_id')
    credit = Decimal()
    date = Date()
    description = Unicode(null=True)
    id = Integer64(primary_key=True)
    refill_type = Integer32()


class MessageAgent(TableModel):
    __tablename__ = 'cc_message_agent'

    id = Integer64(primary_key=True)
    id_agent = Integer32()
    logo = Integer32()
    message = Unicode(null=True)
    order_display = Integer32()
    type = Integer32()


class Monitor(TableModel):
    __tablename__ = 'cc_monitor'

    description = Unicode(1, null=True)
    dial_code = Integer32(null=True)
    enable = Integer32()
    id = Integer64(primary_key=True)
    label = Unicode(1, )
    query = Unicode(1, null=True)
    query_type = Integer32()
    result_type = Integer32()
    text_intro = Unicode(1, null=True)


class Notification(TableModel):
    __tablename__ = 'cc_notification'

    date = Date()
    from_ = Integer64(db_column='from_id', null=True)
    from_type = Integer32()
    id = Integer64(primary_key=True)
    key_value = Unicode(1, null=True)
    link = Integer64(db_column='link_id', null=True)
    link_type = Unicode(1, null=True)
    priority = Integer32()


class NotificationAdmin(TableModel):
    __tablename__ = 'cc_notification_admin'

    id_admin = Integer32()
    id_notification = Integer64()
    viewed = Integer32()



class OutboundCidGroup(TableModel):
    __tablename__ = 'cc_outbound_cid_group'

    creationdate = Date()
    group_name = Unicode(1, )


class OutboundCidList(TableModel):
    __tablename__ = 'cc_outbound_cid_list'

    activated = Integer32()
    cid = Unicode(1, null=True)
    creationdate = Date()
    outbound_cid_group = Integer32()




class PackageGroup(TableModel):
    __tablename__='cc_package_group'

    description = Unicode(null=True)
    name = Unicode(1, )


class PackageOffer(TableModel):
    __tablename__='cc_package_offer'

    billingtype = Integer32()
    creationdate = Date()
    freetimetocall = Integer32()
    id = Integer64(primary_key=True)
    label = Unicode(1, )
    packagetype = Integer32()
    startday = Integer32()


class PackageRate(TableModel):
    __tablename__ = 'cc_package_rate'

    package = Integer32(db_column='package_id')
    rate = Integer32(db_column='rate_id')



class PackgroupPackage(TableModel):
    __tablename__ = 'cc_packgroup_package'

    package = Integer32(db_column='package_id')
    packagegroup = Integer32(db_column='packagegroup_id')

class PaymentMethods(TableModel):
    __tablename__ = 'cc_payment_methods'

    payment_filename = Unicode(1, )
    payment_method = Unicode(1, )


class Payments(TableModel):
    __tablename__ = 'cc_payments'

    cc_expires = Unicode(1, null=True)
    cc_number = Unicode(1, null=True)
    cc_owner = Unicode(1, null=True)
    cc_type = Unicode(1, null=True)
    currency = Unicode(1, null=True)
    currency_value = Decimal(null=True)
    customers_email_address = Unicode(1, )
    customers = Integer64(db_column='customers_id')
    customers_name = Unicode(1, )
    date_purchased = Date(null=True)
    id = Integer64(primary_key=True)
    item = Unicode(1, db_column='item_id', null=True)
    item_name = Unicode(1, null=True)
    item_quantity = Integer32()
    last_modified = Date(null=True)
    orders_amount = Decimal(null=True)
    orders_date_finished = Date(null=True)
    orders_status = Integer32()
    payment_method = Unicode(1, )

class PaymentsAgent(TableModel):
    __tablename__ = 'cc_payments_agent'

    agent_email_address = Unicode(1, )
    agent = Integer64(db_column='agent_id')
    agent_name = Unicode(1, )
    cc_expires = Unicode(1, null=True)
    cc_number = Unicode(1, null=True)
    cc_owner = Unicode(1, null=True)
    cc_type = Unicode(1, null=True)
    currency = Unicode(1, null=True)
    currency_value = Decimal(null=True)
    date_purchased = Date(null=True)
    id = Integer64(primary_key=True)
    item = Unicode(1, db_column='item_id', null=True)
    item_name = Unicode(1, null=True)
    item_quantity = Integer32()
    last_modified = Date(null=True)
    orders_amount = Decimal(null=True)
    orders_date_finished = Date(null=True)
    orders_status = Integer32()
    payment_method = Unicode(1, )

class PaymentsStatus(TableModel):
    __tablename__ = 'cc_payments_status'

    status = Integer32(db_column='status_id')
    status_name = Unicode(1, )


class Paypal(TableModel):
    __tablename__ = 'cc_paypal'

    address_city = Unicode(1, )
    address_country = Unicode(1, )
    address_name = Unicode(1, )
    address_state = Unicode(1, )
    address_status = Unicode(1, )
    address_street = Unicode(1, )
    address_zip = Unicode(1, )
    first_name = Unicode(1, null=True)
    item_name = Unicode(1, null=True)
    item_number = Unicode(1, null=True)
    last_name = Unicode(1, null=True)
    mc_currency = Unicode(1, null=True)
    mc_fee = Decimal(null=True)
    mc_gross = Decimal(null=True)
    memo = Unicode(null=True)
    payer_business_name = Unicode(1, )
    payer_email = Unicode(1, null=True)
    payer = Unicode(1, db_column='payer_id', null=True)
    payer_status = Unicode(1, null=True)
    payment_date = Unicode(1, null=True)
    payment_status = Unicode(1, )
    payment_type = Unicode(1, null=True)
    pending_reason = Unicode(1, )
    quantity = Integer32()
    reason_code = Unicode(1, )
    tax = Decimal(null=True)
    txn = Unicode(1, db_column='txn_id', null=True, unique=True)
    txn_type = Unicode(1, )


class Phonebook(TableModel):
    __tablename__ = 'cc_phonebook'

    description = Unicode(null=True)
    id_card = Integer64()
    name = Unicode(1, )


class Phonenumber(TableModel):
    __tablename__ = 'cc_phonenumber'

    amount = Integer32()
    creationdate = Date()
    id = Integer64(primary_key=True)
    id_phonebook = Integer32()
    info = Unicode(null=True)
    name = Unicode(1, null=True)
    number = Unicode(1, )
    status = Integer32()


class Prefix(TableModel):
    __tablename__ = 'cc_prefix'

    destination = Unicode(1, index=True)
    prefix = Integer64(primary_key=True)


class Provider(TableModel):
    __tablename__ = 'cc_provider'

    creationdate = Date()
    description = Unicode(null=True)
    provider_name = Unicode(1, unique=True)

class Ratecard(TableModel):
    __tablename__ = 'cc_ratecard'

    additional_block_charge = Decimal()
    additional_block_charge_time = Integer32()
    additional_grace = Integer32()
    announce_time_correction = Decimal()
    billingblock = Integer32()
    billingblocka = Integer32()
    billingblockb = Integer32()
    billingblockc = Integer32()
    buyrate = Decimal()
    buyrateincrement = Integer32()
    buyrateinitblock = Integer32()
    chargea = Decimal()
    chargeb = Decimal()
    chargec = Float()
    connectcharge = Decimal()
    destination = Integer64(null=True)
    dialprefix = Unicode(1, index=True)
    disconnectcharge = Decimal()
    disconnectcharge_after = Integer32()
    endtime = Integer32(null=True)
    id_outbound_cidgroup = Integer32(null=True)
    id_trunk = Integer32(null=True)
    idtariffplan = Integer32(index=True)
    initblock = Integer32()
    is_merged = Integer32(null=True)
    minimal_cost = Decimal()
    musiconhold = Unicode(1, )
    rateinitial = Decimal()
    rounding_calltime = Integer32()
    rounding_threshold = Integer32()
    startdate = Date()
    starttime = Integer32(null=True)
    stepchargea = Decimal()
    stepchargeb = Decimal()
    stepchargec = Float()
    stopdate = Date()
    tag = Unicode(1, null=True)
    timechargea = Integer32()
    timechargeb = Integer32()
    timechargec = Integer32()


class Receipt(TableModel):
    __tablename__ = 'cc_receipt'

    date = Date()
    description = Unicode()
    id = Integer64(primary_key=True)
    id_card = Integer64()
    status = Integer32()
    title = Unicode(1, )


class ReceiptItem(TableModel):
    __tablename__ = 'cc_receipt_item'

    date = Date()
    description = Unicode()
    id = Integer64(primary_key=True)
    id_ext = Integer64(null=True)
    id_receipt = Integer64()
    price = Decimal()
    type_ext = Unicode(1, null=True)


class RemittanceRequest(TableModel):
    __tablename__ = 'cc_remittance_request'

    amount = Decimal()
    date = Date()
    id = Integer64(primary_key=True)
    id_agent = Integer64()
    status = Integer32()
    type = Integer32()


class RestrictedPhonenumber(TableModel):
    __tablename__ = 'cc_restricted_phonenumber'

    id = Integer64(primary_key=True)
    id_card = Integer64()
    number = Unicode(1, )


class ServerGroup(TableModel):
    __tablename__ = 'cc_server_group'

    description = Unicode(null=True)
    id = Integer64(primary_key=True)
    name = Unicode(1, null=True)


class ServerManager(TableModel):
    __tablename__ = 'cc_server_manager'

    id = Integer64(primary_key=True)
    id_group = Integer32(null=True)
    lasttime_used = Date()
    manager_host = Unicode(1, null=True)
    manager_secret = Unicode(1, null=True)
    manager_username = Unicode(1, null=True)
    server_ip = Unicode(1, null=True)


class Service(TableModel):
    __tablename__ = 'cc_service'

    amount = Float()
    datecreate = Date()
    datelastrun = Date()
    daynumber = Integer32()
    dialplan = Integer32(null=True)
    emailreport = Unicode(1, )
    id = Integer64(primary_key=True)
    maxnumbercycle = Integer32()
    name = Unicode(1, )
    numberofrun = Integer32()
    operate_mode = Integer32(null=True)
    period = Integer32()
    rule = Integer32()
    status = Integer32()
    stopmode = Integer32()
    totalcardperform = Integer32()
    totalcredit = Float()
    use_group = Integer32(null=True)


class ServiceReport(TableModel):
    __tablename__ = 'cc_service_report'

    cc_service = Integer64(db_column='cc_service_id')
    daterun = Date()
    id = Integer64(primary_key=True)
    totalcardperform = Integer32(null=True)
    totalcredit = Float(null=True)


class SipBuddies(TableModel):
    __tablename__ = 'cc_sip_buddies'

    defaultip = Unicode(1, db_column='DEFAULTip', null=True)
    accountcode = Unicode(1, )
    allow = Unicode(1, )
    allowtransfer = Unicode(1, )
    amaflags = Unicode(1, null=True)
    auth = Unicode(1, )
    autoframing = Unicode(1, )
    callbackextension = Unicode(1, null=True)
    callerid = Unicode(1, )
    callgroup = Unicode(1, null=True)
    callingpres = Unicode(1, )
    cancallforward = Unicode(1, null=True)
    canreinvite = Unicode(1, )
    cid_number = Unicode(1, )
    context = Unicode(1, )
    defaultuser = Unicode(1, )
    deny = Unicode(1, )
    disallow = Unicode(1, )
    dtmfmode = Unicode(1, )
    fromdomain = Unicode(1, )
    fromuser = Unicode(1, )
    fullcontact = Unicode(1, )
    host = Unicode(1, index=True)
    id_cc_card = Integer32()
    incominglimit = Unicode(1, )
    insecure = Unicode(1, )
    ipaddr = Unicode(1, index=True)
    language = Unicode(1, null=True)
    lastms = Unicode(1, null=True)
    mailbox = Unicode(1, )
    mask = Unicode(1, )
    maxcallbitrate = Unicode(1, )
    md5secret = Unicode(1, )
    mohsuggest = Unicode(1, )
    musicclass = Unicode(1, )
    musiconhold = Unicode(1, )
    name = Unicode(1, unique=True)
    nat = Unicode(1, null=True)
    outboundproxy = Unicode(1, )
    permit = Unicode(1, null=True)
    pickupgroup = Unicode(1, null=True)
    port = Unicode(1, index=True)
    qualify = Unicode(1, null=True)
    regexten = Unicode(1, )
    regseconds = Integer32()
    regserver = Unicode(1, null=True)
    restrictcid = Unicode(1, null=True)
    rtpholdtimeout = Unicode(1, null=True)
    rtpkeepalive = Unicode(1, )
    rtptimeout = Unicode(1, null=True)
    secret = Unicode(1, )
    setvar = Unicode(1, )
    subscribecontext = Unicode(1, )
    subscribemwi = Unicode(1, )
    type = Unicode(1, )
    useragent = Unicode(1, null=True)
    usereqphone = Unicode(1, )
    username = Unicode(1, )
    vmexten = Unicode(1, )


class SipBuddiesEmpty(TableModel):
    __tablename__ = 'cc_sip_buddies_empty'

    defaultip = Unicode(1, db_column='DEFAULTip', null=True)
    accountcode = Unicode(1, )
    allow = Unicode(1, )
    amaflags = Unicode(1, null=True)
    callerid = Unicode(1, )
    callgroup = Unicode(1, null=True)
    cancallforward = Unicode(1, null=True)
    canreinvite = Unicode(1, )
    context = Unicode(1, )
    deny = Unicode(1, )
    disallow = Unicode(1, )
    dtmfmode = Unicode(1, )
    fromdomain = Unicode(1, )
    fromuser = Unicode(1, )
    fullcontact = Unicode(1, )
    host = Unicode(1, )
    id = Integer32()
    id_cc_card = Integer32()
    insecure = Unicode(1, )
    ipaddr = Unicode(1, )
    language = Unicode(1, null=True)
    mailbox = Unicode(1, )
    mask = Unicode(1, )
    md5secret = Unicode(1, )
    musiconhold = Unicode(1, )
    name = Unicode(1, )
    nat = Unicode(1, null=True)
    permit = Unicode(1, null=True)
    pickupgroup = Unicode(1, null=True)
    port = Unicode(1, )
    qualify = Unicode(1, null=True)
    regexten = Unicode(1, )
    regseconds = Integer32()
    restrictcid = Unicode(1, null=True)
    rtpholdtimeout = Unicode(1, null=True)
    rtptimeout = Unicode(1, null=True)
    secret = Unicode(1, )
    setvar = Unicode(1, )
    type = Unicode(1, )
    username = Unicode(1, )


class Speeddial(TableModel):
    __tablename__ = 'cc_speeddial'

    creationdate = Date()
    id = Integer64(primary_key=True)
    id_cc_card = Integer64()
    name = Unicode(1, )
    phone = Unicode(1, )
    speeddial = Integer32(null=True)


class StatusLog(TableModel):
    __tablename__ = 'cc_status_log'

    id = Integer64(primary_key=True)
    id_cc_card = Integer64()
    status = Integer32()
    updated_date = Date()


class SubscriptionService(TableModel):
    __tablename__ = 'cc_subscription_service'

    datecreate = Date()
    datelastrun = Date()
    emailreport = Unicode(1, )
    fee = Float()
    id = Integer64(primary_key=True)
    label = Unicode(1, )
    numberofrun = Integer32()
    startdate = Date()
    status = Integer32()
    stopdate = Date()
    totalcardperform = Integer32()
    totalcredit = Float()


class SubscriptionSignup(TableModel):
    __tablename__ = 'cc_subscription_signup'

    description = Unicode(1, null=True)
    enable = Integer32()
    id = Integer64(primary_key=True)
    id_callplan = Integer64(null=True)
    id_subscription = Integer64(null=True)
    label = Unicode(1, )


class Support(TableModel):
    __tablename__ = 'cc_support'

    email = Unicode(1, null=True)
    language = Unicode(1, )
    name = Unicode(1, )


class SupportComponent(TableModel):
    __tablename__ = 'cc_support_component'

    activated = Integer32()
    id_support = Integer32()
    name = Unicode(1, )
    type_user = Integer32()


class SystemLog(TableModel):
    __tablename__ = 'cc_system_log'

    action = Unicode()
    agent = Integer32(null=True)
    creationdate = Date()
    data = Unicode(null=True)
    description = Unicode(null=True)
    iduser = Integer32()
    ipaddress = Unicode(1, null=True)
    loglevel = Integer32()
    pagename = Unicode(1, null=True)
    tablename = Unicode(1, null=True)


class Tariffgroup(TableModel):
    __tablename__ = 'cc_tariffgroup'

    creationdate = Date()
    id_cc_package_offer = Integer64()
    idtariffplan = Integer32()
    iduser = Integer32()
    lcrtype = Integer32()
    removeinterprefix = Integer32()
    tariffgroupname = Unicode(1, )


class TariffgroupPlan(TableModel):
    __tablename__ = 'cc_tariffgroup_plan'

    idtariffgroup = Integer32()
    idtariffplan = Integer32()

class Tariffplan(TableModel):
    __tablename__ = 'cc_tariffplan'

    calleridprefix = Unicode(1, )
    creationdate = Date()
    description = Unicode(null=True)
    dnidprefix = Unicode(1, )
    expirationdate = Date()
    id_trunk = Integer32(null=True)
    idowner = Integer32(null=True)
    iduser = Integer32()
    reftariffplan = Integer32(null=True)
    secondusedcarrier = Integer32(null=True)
    secondusedratecard = Integer32(null=True)
    secondusedreal = Integer32(null=True)
    startingdate = Date()
    tariffname = Unicode(1, )

class Templatemail(TableModel):
    __tablename__ = 'cc_templatemail'

    fromemail = Unicode(1, null=True)
    fromname = Unicode(1, null=True)
    id_language = Unicode(1, )
    mailtype = Unicode(1, null=True)
    messagehtml = Unicode(1, null=True)
    messagetext = Unicode(1, null=True)
    subject = Unicode(1, null=True)

class Ticket(TableModel):
    __tablename__ = 'cc_ticket'

    creationdate = Date()
    creator = Integer64()
    creator_type = Integer32()
    description = Unicode(null=True)
    id = Integer64(primary_key=True)
    id_component = Integer32()
    priority = Integer32()
    status = Integer32()
    title = Unicode(1, )
    viewed_admin = Integer32()
    viewed_agent = Integer32()
    viewed_cust = Integer32()


class TicketComment(TableModel):
    __tablename__ = 'cc_ticket_comment'

    creator = Integer64()
    creator_type = Integer32()
    date = Date()
    description = Unicode(null=True)
    id = Integer64(primary_key=True)
    id_ticket = Integer64()
    viewed_admin = Integer32()
    viewed_agent = Integer32()
    viewed_cust = Integer32()


class Timezone(TableModel):
    __tablename__ = 'cc_timezone'

    gmtoffset = Integer64()
    gmttime = Unicode(1, null=True)
    gmtzone = Unicode(1, null=True)

class Trunk(TableModel):
    __tablename__ = 'cc_trunk'

    addparameter = Unicode(1, null=True)
    creationdate = Date()
    failover_trunk = Integer32(null=True)
    id_provider = Integer32(null=True)
    id_trunk = PrimaryKeyField()
    if_max_use = Integer32(null=True)
    inuse = Integer32(null=True)
    maxuse = Integer32(null=True)
    providerip = Unicode(1, )
    providertech = Unicode(1, )
    removeprefix = Unicode(1, null=True)
    secondusedcarrier = Integer32(null=True)
    secondusedratecard = Integer32(null=True)
    secondusedreal = Integer32(null=True)
    status = Integer32(null=True)
    trunkcode = Unicode(1, null=True)
    trunkprefix = Unicode(1, null=True)


class UiAuthen(TableModel):
    __tablename__ = 'cc_ui_authen'

    city = Unicode(1, null=True)
    confaddcust = Integer32(null=True)
    country = Unicode(1, null=True)
    datecreation = Date()
    direction = Unicode(1, null=True)
    email = Unicode(1, null=True)
    fax = Unicode(1, null=True)
    groupid = Integer32(null=True)
    login = Unicode(1, unique=True)
    name = Unicode(1, null=True)
    perms = Integer32(null=True)
    phone = Unicode(1, null=True)
    pwd_encoded = Unicode(1, )
    state = Unicode(1, null=True)
    userid = Integer64(primary_key=True)
    zipcode = Unicode(1, null=True)



class Version(TableModel):
    __tablename__ = 'cc_version'
    version = Unicode(1, )


class Voucher(TableModel):
    __tablename__ = 'cc_voucher'

    activated = Unicode(1, )
    creationdate = Date()
    credit = Float()
    currency = Unicode(1, null=True)
    expirationdate = Date()
    id = Integer64(primary_key=True)
    tag = Unicode(1, null=True)
    used = Integer32(null=True)
    usedate = Date()
    usedcardnumber = Unicode(1, null=True)
    voucher = Unicode(1, unique=True)

class Cdrs(TableModel):
    __tablename__ = 'cdrs'

    call_start_time = Date()
    cdr = Integer64(db_column='cdr_id', primary_key=True)
    cost = Integer32()
    created = Date()
    dst_domain = Unicode(1, )
    dst_ousername = Unicode(1, )
    dst_username = Unicode(1, )
    duration = Integer32()
    rated = Integer32()
    sip_call = Unicode(1, db_column='sip_call_id')
    sip_from_tag = Unicode(1, )
    sip_to_tag = Unicode(1, )
    src_domain = Unicode(1, )
    src_ip = Unicode(1, )
    src_username = Unicode(1, )



class CollectionCdrs(TableModel):
    __tablename__ = 'collection_cdrs'

    call_start_time = Date()
    cdr = Integer64(db_column='cdr_id')
    cost = Integer32()
    dst_domain = Unicode(1, )
    dst_ousername = Unicode(1, )
    dst_username = Unicode(1, )
    duration = Integer32()
    flag_imported = Integer32()
    id = Integer64(primary_key=True)
    rated = Integer32()
    sip_call = Unicode(1, db_column='sip_call_id')
    sip_code = Unicode(1, )
    sip_from_tag = Unicode(1, )
    sip_reason = Unicode(1, )
    sip_to_tag = Unicode(1, )
    src_domain = Unicode(1, )
    src_ip = Unicode(1, )
    src_username = Unicode(1, )


class MissedCalls(TableModel):
    __tablename__ = 'missed_calls'

    callid = Unicode(1, index=True)
    cdr = Integer32(db_column='cdr_id')
    dst_domain = Unicode(1, )
    dst_ouser = Unicode(1, )
    dst_user = Unicode(1, )
    from_tag = Unicode(1, )
    method = Unicode(1, )
    sip_code = Unicode(1, )
    sip_reason = Unicode(1, )
    src_domain = Unicode(1, )
    src_ip = Unicode(1, )
    src_user = Unicode(1, )
    time = Date()
    to_tag = Unicode(1, )


class Note(TableModel):
    __tablename__ = 'note'

    created = Date()
    message = Unicode()


class User(TableModel):
    __tablename__ = 'user'

    active = Integer32()
    admin = Integer32()
    email = Unicode(1, unique=True)
    password = Unicode(1, )
    username = Unicode(1, unique=True)

