'''
Created on 1 Jun 2021

@author: jacklok
'''

from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel, FullTextSearchable
from trexmodel.models.datastore.user_models import User
from trexmodel.models.datastore.merchant_models import MerchantAcct, Outlet, MerchantUser
from trexmodel.models.datastore.program_models import MerchantProgram
from trexmodel.models.datastore.voucher_models import MerchantVoucher
from trexlib.utils.string_util import is_empty, is_not_empty
import logging, json
from trexmodel import conf, program_conf
from trexlib.utils.string_util import random_string
from datetime import datetime, timedelta
from trexmodel.utils.model.model_util import generate_transaction_id,\
    string_to_key_property
from trexmodel.conf import SERVER_DATETIME_GMT, HANDLE_DATETIME_WITH_GMT
from trexmodel.models.datastore.reward_models import CustomerPointReward,\
    CustomerStampReward, CustomerEntitledVoucher
from trexmodel.models.datastore.model_decorators import model_transactional


logger = logging.getLogger('model')


class CustomerRedemption(BaseNModel, DictModel):
    '''
    Customer as ancestor
    '''
    
    merchant_acct               = ndb.KeyProperty(name="merchant_acct", kind=MerchantAcct)
    user_acct                   = ndb.KeyProperty(name="user_acct", kind=User)
    redeemed_outlet             = ndb.KeyProperty(name="transact_outlet", kind=Outlet)
    
    reward_format               = ndb.StringProperty(required=True)
    redeem_amount               = ndb.FloatProperty(required=True, default=1)
    
    redeemed_summary            = ndb.JsonProperty(required=True)
    
    transaction_id              = ndb.StringProperty(required=True)
    invoice_id                  = ndb.StringProperty(required=False)
    remarks                     = ndb.StringProperty(required=False)
    
    status                      = ndb.StringProperty(required=True, default=program_conf.REDEEM_STATUS_VALID)
    
    redeemed_datetime           = ndb.DateTimeProperty(required=True, auto_now_add=True)
    redeemed_by                 = ndb.KeyProperty(name="redeemed_by", kind=MerchantUser)
    redeemed_by_username        = ndb.StringProperty(required=False)
    
    reverted_datetime           = ndb.DateTimeProperty(required=False)
    reverted_by                 = ndb.KeyProperty(name="reverted_by", kind=MerchantUser)
    reverted_by_username        = ndb.StringProperty(required=False)
    
    @staticmethod
    def list_by_transaction_id(cls, transaction_id):
        return cls.query(cls.transaction_id==transaction_id).fetch(limit=conf.MAX_FETCH_RECORD)
    
    @property
    def is_valid(self):
        return self.status == program_conf.REDEEM_STATUS_VALID
    
    @property
    def is_revert(self):
        return self.status == program_conf.REDEEM_STATUS_REVERTED
    
    @property
    def redeemed_voucher_keys_list(self):
        return self.redeemed_summary.get('vouchers') 
    
    @property
    def redeemed_voucher_keys_list_in_str(self):
        vourchers =  self.redeemed_summary.get('vouchers')
        if vourchers:
            return json.dumps(vourchers)
        else:
            return ''
    
    @property
    def redeemed_merchant_acct(self):
        return MerchantAcct.fetch(self.merchant_acct.urlsafe())
    
    @property
    def redeemed_merchant_acct_key(self):
        return self.merchant_acct.urlsafe().decode('utf-8')
    
    @property
    def redeemed_outlet_key(self):
        return self.redeemed_outlet.urlsafe().decode('utf-8')
    
    @property
    def redeemed_customer_key(self):
        return self.parent_key
    
    @property
    def redeem_format_label(self):
        pass
    
    def revert(self, reverted_by, reverted_datetime=None):
        self.status = program_conf.REWARD_STATUS_REVERTED
        if reverted_datetime is None:
            reverted_datetime = datetime.now()
        
        self.reverted_datetime      = reverted_datetime
        self.reverted_by            = reverted_by.create_ndb_key()
        self.reverted_by_username   = reverted_by.username
        self.put()
    
    @staticmethod
    def list_by_customer(customer, status=program_conf.REWARD_STATUS_VALID, limit = conf.MAX_FETCH_RECORD):
        return CustomerRedemption.query(ndb.AND(CustomerRedemption.status==status), ancestor=customer.create_ndb_key()).fetch(limit=limit)
    
    @staticmethod
    def create(customer, reward_format, redeem_amount, redeemed_outlet, 
               redeemed_voucher_keys_list=None, invoice_id=None, remarks=None, redeemed_by=None, redeemed_datetime=None):
        
        reward_summary              = customer.reward_summary
        entitled_voucher_summary    = customer.entitled_voucher_summary
        
        if is_not_empty(redeemed_by):
            if isinstance(redeemed_by, MerchantUser):
                redeemed_by_username = redeemed_by.username

        
        transaction_id = generate_transaction_id(prefix='r')
        
        if redeemed_datetime is None:
            redeemed_datetime = datetime.now()
            if HANDLE_DATETIME_WITH_GMT:
                redeemed_datetime = redeemed_datetime - timedelta(hours=int(SERVER_DATETIME_GMT))
        
        redeemed_summary = {}
        
        @model_transactional(desc='redeem reward')
        def __start_redeem(__customer, __total_redeemed_amount, cursor, reward_cls):
            (result, next_cursor) = reward_cls.list_by_valid_with_cursor(__customer, limit=50, start_cursor=cursor)
            
            if result:
                for r in result:
                    reward_balance = r.reward_balance
                    if reward_balance<__total_redeemed_amount:
                        total_redeemed_amount -=reward_balance
                        r.update_used_reward_amount(reward_balance)
                    else:
                        __total_redeemed_amount = 0
                        after_deduce_reward_balance = reward_balance - __total_redeemed_amount
                        r.update_used_reward_amount(after_deduce_reward_balance)
                    
                    if __total_redeemed_amount==0:
                        break
                
                return (__total_redeemed_amount, next_cursor)
            else:
                raise Exception('Reward not found')
        
        if reward_format == program_conf.REWARD_FORMAT_POINT:
            total_redeemed_amount = redeem_amount
            cursor = None
             
            while total_redeemed_amount>0:
                (total_redeemed_amount, cursor) = __start_redeem(customer, total_redeemed_amount, cursor, CustomerPointReward)
            
            
            redeemed_summary = {
                                reward_format : redeem_amount,
                                }
            
            reward_summary = {
                                reward_format : reward_summary.get(reward_format) -  redeem_amount
                                }
            
        elif reward_format == program_conf.REWARD_FORMAT_STAMP:
            total_redeemed_amount = redeem_amount
            cursor = None
             
            while total_redeemed_amount>0:
                (total_redeemed_amount, cursor) = __start_redeem(customer, total_redeemed_amount, cursor, CustomerStampReward)
             
            redeemed_summary = {
                                reward_format : redeem_amount,
                                }
            
            reward_summary = {
                                reward_format : reward_summary.get(reward_format) -  redeem_amount
                                }
            
        elif reward_format == program_conf.REWARD_FORMAT_VOUCHER:
            redeemed_summary = {
                                'vouchers' :   {
                                                }
                                }
            
            for v_k in redeemed_voucher_keys_list:
                customer_voucher        = CustomerEntitledVoucher.fetch(v_k)
                entitled_voucher_key    = customer_voucher.entitled_voucher_key
                redeemed_voucher_count  = redeemed_summary.get('vouchers').get(entitled_voucher_key)
                 
                if redeemed_voucher_count:
                    redeemed_summary.get('vouchers')[entitled_voucher_key] +=1
                else:
                    redeemed_summary.get('vouchers')[entitled_voucher_key] =1
                
                customer_voucher.redeem(redeemed_by, redeemed_datetime=redeemed_datetime)
                
                logger.debug('Voucher(%s) have been redeemed', customer_voucher.redeem_code)
                
            
            for v_k, v_c in  redeemed_summary.get('vouchers').items():
                entitled_voucher_summary[v_k] -= v_c
        
        
        customer_redemption = CustomerRedemption(
                                                    parent                  = customer.create_ndb_key(),
                                                    user_acct               = customer.registered_user_acct.create_ndb_key(),
                                                    merchant_acct           = customer.registered_merchant_acct.create_ndb_key(),
                                                    redeemed_outlet         = redeemed_outlet.create_ndb_key(),
                                                    reward_format           = reward_format,
                                                    redeem_amount           = redeem_amount,
                                                    redeemed_summary        = redeemed_summary,
                                                    
                                                    transaction_id          = transaction_id,
                                                    invoice_id              = invoice_id,
                                                    remarks                 = remarks,
                                                    
                                                    redeemed_by             = redeemed_by.create_ndb_key(),
                                                    redeemed_by_username    = redeemed_by_username,
                                                    
                                                    redeemed_datetime       = redeemed_datetime,
                                                    
                                                    )
        
        
        customer_redemption.put()
        
        customer.reward_summary             = reward_summary
        customer.entitled_voucher_summary   = entitled_voucher_summary
        customer.put()
        
        return customer_redemption
    
