from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, BackgroundTasks
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from SERVICE_dir.jwt_logic import JWTParamas, create_access_token, create_refresh_token, TokenPayload
from .api_routes import APIRoutes
from MODELS_dir import acc_model as AccountModel
from SERVICE_dir.serivce_manipulator_account import ServiceManipulatorACCOUNT as SMa
from starlette.responses import RedirectResponse


account_app = APIRouter(tags=["ACCOUNT FUNCTIONALITY"])


""" #################################
                   START
            TOKEN FUNCTIONALITY                             
    #################################
"""
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/signin",
    scheme_name="JWT"
)


"""
##############################
RETURN TOKEN OF CURRENT USER IF ALL ARE OK
IN FUTURE WILL DECODE AND GET ID OF CLIENT
##############################
"""


async def get_current_user(token: str = Depends(reuseable_oauth)):
    """CHECK INVALID TOKENS
       CHECK EXPIRED TOKENS"""
    try:
        payload = jwt.decode(
            token, JWTParamas.ACCESS_SECRET_KEY, algorithms=[JWTParamas.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.exp < datetime.utcnow().replace(tzinfo=timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ERROR",
                headers={"WWW-Authenticate": "EXPIRED TIME"},
            )
        return token
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ERROR",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def update_token_of_user(account_id, access_token):
    SMa.auto_update_token_for_account(account_id=account_id, access_token=access_token)


async def send_verify_email(*arg):
    SMa.call_async_function(acc_email=arg[0], generated_link=arg[1])

""" #################################
                   END
            TOKEN FUNCTIONALITY                             
    #################################
"""



""" --------------START ACCOUNT API-s---------------
--- account signup 
--- account signin
--- account verify
--- account recovery code send
--- account recovery code check
--- account new password setting
"""


@account_app.post(APIRoutes.acc_register_route)
async def acc_signup(acc_reg_model: AccountModel.AccountRegModel, back_task: BackgroundTasks):
    """AcRM is account registration model
    REGISTRATION API"""
    tmp = await SMa.post_acc_into_temp_db(temp_acc_model=acc_reg_model)
    if tmp is not None:
        if tmp == "ka":
            raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'REGISTR DATA ERROR'})
        back_task.add_task(send_verify_email, tmp[0], tmp[1])
        return {"status": "REGISTERED"}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'REGISTR ERROR'})


@account_app.get(APIRoutes.acc_verify_route)
async def acc_verify(token_verify: str, data: str):
    """VERIFY ACCOUNT SENDING EMAIL"""
    temp_ = SMa.verify_link(verify_token=token_verify)
    if temp_ is not None:
        if SMa.send_unique_code_and_pass(acc_unique_id=temp_[0], acc_email=temp_[1]):
            redirect_page = RedirectResponse("http://pcassa.ru/")
            return redirect_page
        #add html page for errors
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'VERIFY ERROR'})


@account_app.post(APIRoutes.acc_recovery_route+'sendemail')
async def acc_recovery_sender(receiver_email: AccountModel.AccRecoveryEmail):
    """SEND CODE TO EMAIL FOR RECOVERY
        GET recovery code and save it"""
    tmp_ = SMa.recovery_code(receiver_email=receiver_email.receiver_email)
    if tmp_ is not None:
        return {"status": "OK", "data": "VERIFY CODE SENDED"}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'VERIFY CODE ERROR'})


@account_app.post(APIRoutes.acc_recovery_route)
async def acc_recovery_checker(item_for_verify: AccountModel.AccountVerifyModel):
    """ CHECK CODE FOR RECOVERY"""
    if SMa.recovery_code_checker(
            code_for_verify=item_for_verify.code_for_verify,
            receiver_email=item_for_verify.receiver_email):
        return {"status": "OK", "data": "VERIFY CODE VALID"}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'CODE ERROR'})


@account_app.post(APIRoutes.acc_update_pass)
async def acc_update_pass(acc_rec_model: AccountModel.AccountRecModel):
    """ UPDATE PASS OF USER """
    if SMa.update_acc_pass(
            acc_email=acc_rec_model.acc_email,
            acc_new_pass=acc_rec_model.acc_new_pass):
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'UPDATE ERROR'})


@account_app.post(APIRoutes.acc_login_route)
async def signin_acc(acc_sign_model: OAuth2PasswordRequestForm = Depends()):
    """ SIGNIN CHECKING RETURN TOKENS """
    check_ = SMa.signin_acc(
        acc_email=acc_sign_model.username,
        acc_pass=acc_sign_model.password,)
    if check_ is not None:
        id_ = check_['c_id']
        ACCESS_TOKEN = create_access_token(id_)
        REFRESH_TOKEN = create_refresh_token(id_)
        if SMa.add_access_token_to_account(
                access_token=ACCESS_TOKEN,
                account_id=check_['c_id']):

            return {
                "access_token": ACCESS_TOKEN,
                "refresh_token": REFRESH_TOKEN
            }
        raise HTTPException(status_code=401, detail="ERROR", headers={'status': 'TOKEN ADD ERROR'})
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'SIGNIN ERROR'})


@account_app.post(APIRoutes.acc_refresh_token)
def check_and_send_new_token(
                       refresh_token: str,
                       callback_after_successful_cheking: BackgroundTasks,
                       access_token: OAuth2PasswordBearer = Depends(get_current_user),
                       ):
    """CHECK SENDED REFRESH TOKEN AFTER
       THIS REFRESH ALL TOKENS AND SEND NEW"""
    try:
        #decode refresh token and get all information about client
        refresh_decoded_dict = jwt.decode(refresh_token,
                                  JWTParamas.REFRESH_SECRET_KEY,
                                  JWTParamas.ALGORITHM)
        refresh_info = TokenPayload(**refresh_decoded_dict)
        refresh_timeout = refresh_info.exp
        refresh_id = refresh_info.sub.replace(JWTParamas.SOLD_KEY, "")
        now_ = datetime.utcnow().replace(tzinfo=timezone.utc)
        #check time of refresh_token
        if now_ < refresh_timeout:
            if SMa.check_refresh_token(client_id=refresh_id,
                                       client_refresh_token=refresh_token):
                access_token_ = create_access_token(refresh_id)
                refresh_token_ = create_refresh_token(refresh_id)
                #update db with new token
                callback_after_successful_cheking.add_task(
                    update_token_of_user,
                    refresh_id,
                    access_token_)
                return {
                    "access_token": access_token_,
                    "refresh_token": refresh_token_
                }
        raise HTTPException(status_code=401, detail="ERROR", headers={'status': 'TOKEN UPDATE ERROR'})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="ERROR", headers={'status': 'TOKEN UPDATE ERROR'})


@account_app.get(APIRoutes.acc_login_route)
async def signin_acc_info(access_token: OAuth2PasswordBearer = Depends(get_current_user)):
    """GET ACCOUNT INFO WITH TOKENS"""
    check_ = SMa.signin_acc_info(acc_token=access_token)
    if check_ is not None:
        return check_
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'SIGNIN ERROR'})
"""-------------END OF ACCOUNT API-s-----------------"""





