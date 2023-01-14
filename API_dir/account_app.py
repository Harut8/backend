from datetime import datetime, timezone
from fastapi import APIRouter, middleware
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from SERVICE_dir.jwt_logic import JWTParamas, create_access_token, create_refresh_token, TokenPayload
from .api_routes import APIRoutes
from MODELS_dir import acc_model as AccountModel
from SERVICE_dir.serivce_manipulator_account import ServiceManipulatorACCOUNT as SMa
from DB_dir.db_connection import DatabaseConnection
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


async def get_current_user(token: str = Depends(reuseable_oauth)):
    """CHECK INVALID TOKENS
       CHECK EXPIRED TOKENS"""
    try:
        payload = jwt.decode(
            token, JWTParamas.SECRET_KEY, algorithms=[JWTParamas.ALGORITHM]
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


async def get_id_for_refresh(token: str = Depends(reuseable_oauth)):
    """CHECK INVALID TOKENS
       CHECK EXPIRED TOKENS"""
    try:
        payload = jwt.decode(
            token, JWTParamas.SECRET_KEY, algorithms=[JWTParamas.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.exp < datetime.utcnow().replace(tzinfo=timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ERROR",
                headers={"WWW-Authenticate": "EXPIRED TIME"},
            )
        return token_data.sub
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ERROR",
            headers={"WWW-Authenticate": "Bearer"},
        )



""" #################################
                   END
            TOKEN FUNCTIONALITY                             
    #################################
"""


@account_app.on_event('shutdown')
def end_api_background_tasks():
    if SMa.TOKEN_THREAD1 is not None and SMa.TOKEN_THREAD2 is not None:
        SMa.TOKEN_THREAD1.cancel()
        SMa.TOKEN_THREAD2.cancel()
    DatabaseConnection.close()



""" --------------START ACCOUNT API-s---------------
--- account signup 
--- account signin
--- account verify
--- account recovery code send
--- account recovery code check
--- account new password setting
"""


@account_app.post(APIRoutes.acc_register_route)
async def acc_signup(acc_reg_model: AccountModel.AccountRegModel):
    """AcRM is account registration model
    REGISTRATION API"""
    print(acc_reg_model)
    tmp = SMa.post_acc_into_temp_db(temp_acc_model=acc_reg_model)
    if tmp:
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
async def acc_recovery(receiver_email: AccountModel.AccRecoveryEmail):
    """SEND CODE TO EMAIL FOR RECOVERY
        GET recovery code and save it"""
    tmp_ = SMa.recovery_code(receiver_email=receiver_email.receiver_email)
    if tmp_ is not None:
        return {"status": "OK", "data": "VERIFY CODE SENDED"}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'VERIFY CODE ERROR'})


@account_app.post(APIRoutes.acc_recovery_route)
async def acc_recovery(item_for_verify: AccountModel.AccountVerifyModel):
    """ CHECK CODE FOR RECOVERY"""
    if SMa.recovery_code_checker(
            code_for_verify=item_for_verify.code_for_verify,
            receiver_email=item_for_verify.receiver_email):
        return {"status": "OK", "data": "VERIFY CODE VALID"}
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'CODE ERROR'})


@account_app.put(APIRoutes.acc_update_pass)
async def acc_update_pass(acc_rec_model: AccountModel.AccountRecModel):
    """ UPDATE PASS OF USER """
    if SMa.update_acc_pass(
            acc_email=acc_rec_model.acc_email,
            acc_new_pass=acc_rec_model.acc_new_pass):
        return {"status": "UPDATE PASSWORD IS SUCCESSFUL"}
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
                       access_token: OAuth2PasswordBearer = Depends(get_id_for_refresh)
                       ):
    """CHECK SENDED REFRESH TOKEN AFTER
       THIS REFRESH ALL TOKENS AND SEND NEW"""
    if SMa.check_refresh_token(client_refresh_token=refresh_token):
        create_refresh_token(access_token)
        return {
            "access_token": SMa.ACCESS_TOKEN_FOR_CHECK,
            "refresh_token": SMa.REFRESH_TOKEN_FOR_CHECK
        }
    raise HTTPException(status_code=401, detail="ERROR", headers={'status': 'TOKEN UPDATE ERROR'})


@account_app.get(APIRoutes.acc_login_route)
async def signin_acc_info(access_token: OAuth2PasswordBearer = Depends(get_current_user)):
    """GET ACCOUNT INFO WITH TOKENS"""
    check_ = SMa.signin_acc_info(acc_token=access_token)
    if check_ is not None:
        return check_
    raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'SIGNIN ERROR'})
"""-------------END OF ACCOUNT API-s-----------------"""





