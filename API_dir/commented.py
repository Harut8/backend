# from datetime import datetime, timezone
# from fastapi import FastAPI as Fapi
# from fastapi import HTTPException, status, Depends
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import jwt
# from uvicorn import run
#
# from SERVICE_dir.jwt_logic import JWTParamas, create_access_token, create_refresh_token, TokenPayload
# from .api_routes import APIRoutes
# from MODELS_dir import acc_model as AcRM
# from MODELS_dir.tarif_model import (TarifToClient, PersonalTarifForClient)
# from SERVICE_dir.serivce_manipulator_account import ServiceManipulatorACCOUNT as SMa
# from SERVICE_dir.service_manipulator_tarifes import ServiceManipulatorTARIFES as SMt
# from fastapi.middleware.cors import CORSMiddleware
#
# api = Fapi()
#
# origins = ["*"]
#
# api.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# """ #################################
#                    START
#             TOKEN FUNCTIONALITY
#     #################################
# """
# reuseable_oauth = OAuth2PasswordBearer(
#     tokenUrl="/signin",
#     scheme_name="JWT"
# )
#
#
# async def get_current_user(token: str = Depends(reuseable_oauth)):
#     """CHECK INVALID TOKENS
#        CHECK EXPIRED TOKENS"""
#     try:
#         payload = jwt.decode(
#             token, JWTParamas.SECRET_KEY, algorithms=[JWTParamas.ALGORITHM]
#         )
#         token_data = TokenPayload(**payload)
#         if token_data.exp < datetime.utcnow().replace(tzinfo=timezone.utc):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="ERROR",
#                 headers={"WWW-Authenticate": "EXPIRED TIME"},
#             )
#         return token_data
#     except Exception as e:
#         print(e)
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="ERROR",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     #user: Union[dict[str, Any], None] = db.get(token_data.sub, None)
#
#     # if user is None:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_404_NOT_FOUND,
#     #         detail="Could not find user",
#     #     )
#     #
#     # return SystemUser(**user)
#
# """ #################################
#                    END
#             TOKEN FUNCTIONALITY
#     #################################
# """
#
#
# @api.get(APIRoutes.main)
# async def start():
#     return {'SERVER_STATUS': "RUNNING"}
#
#
# @api.on_event('shutdown')
# def end_api_background_tasks():
#     if SMa.TOKEN_THREAD1 is not None and SMa.TOKEN_THREAD2 is not None:
#         SMa.TOKEN_THREAD1.cancel()
#         SMa.TOKEN_THREAD2.cancel()
#
#
# """ --------------START ACCOUNT API-s---------------
# --- account signup
# --- account signin
# --- account verify
# --- account recovery code send
# --- account recovery code check
# --- account new password setting
# """
#
#
# @api.post(APIRoutes.acc_register_route)
# async def acc_signup(acc_reg_model: AcRM.AccountRegModel):
#     """AcRM is account registration model
#     REGISTRATION API"""
#     tmp = SMa.post_acc_into_temp_db(temp_acc_model=acc_reg_model)
#     if tmp:
#         return {"status": "REGISTERED"}
#     else:
#         return {"status": "ERROR"}
#
#
# @api.get(APIRoutes.acc_verify_route)
# async def acc_verify(temp_acc_id: str, data: str):
#     """VERIFY ACCOUNT SENDING EMAIL"""
#     temp_ = SMa.verify_link(temp_id=int(temp_acc_id))
#     if temp_[0]:
#         print(temp_)
#         if SMa.send_unique_code_and_pass(acc_unique_id=temp_[1], acc_email=temp_[2]):
#             return {"status": 'VERIFYING SUCCESS'}
#     else:
#         return {"status": "ERROR"}
#
#
# @api.get(APIRoutes.acc_recovery_route)
# async def acc_recovery(receiver_email: str):
#     """SEND CODE TO EMAIL FOR RECOVERY
#         GET recovery code and save it"""
#     tmp_ = SMa.recovery_code(receiver_email=receiver_email)
#     if tmp_ == False:
#         return {"status": "ERROR"}
#     SMa.recovery_code_var = tmp_
#     return {"status": "CODE SEND"}
#
#
# @api.post(APIRoutes.acc_recovery_route)
# async def acc_recovery(code_for_verify: str):
#     """ CHECK CODE FOR RECOVERY"""
#     if code_for_verify == SMa.recovery_code_var:
#         SMa.recovery_code_var = None
#         return {"status": "VERIFY CODE TRUE"}
#     else:
#         return {"status": "CODE ERROR"}
#
#
# @api.put(APIRoutes.acc_update_pass)
# async def acc_update_pass(acc_rec_model: AcRM.AccountRecModel):
#     """ UPDATE PASS OF USER """
#     if SMa.update_acc_pass(acc_email=acc_rec_model.acc_email, acc_new_pass=acc_rec_model.acc_new_pass):
#         return {"status": "UPDATE PASSWORD IS SUCCESSFUL"}
#     else:
#         return {"status": "UPDATE ERROR"}
#
#
# #AcRM.AccountSignModel
# @api.post(APIRoutes.acc_login_route)
# async def signin_acc(acc_sign_model: OAuth2PasswordRequestForm = Depends()):
#     """ SIGNIN CHECKING RETURN TOKENS """
#     check_ = SMa.signin_acc(
#         acc_email=acc_sign_model.username,
#         acc_pass=acc_sign_model.password,)
#     if check_[0]:
#         ACCESS_TOKEN = create_access_token(check_[1])
#         REFRESH_TOKEN = create_refresh_token(check_[1])
#         if SMa.add_access_token_to_account(
#                 access_token=ACCESS_TOKEN,
#                 account_id=check_[1]['c_id']):
#
#             return {
#                 "access_token": ACCESS_TOKEN,
#                 "refresh_token": REFRESH_TOKEN
#             }
#         raise HTTPException(status_code=401, detail="ERROR", headers={'status': 'TOKEN ADD ERROR'})
#         #return check_[1]
#     else:
#         raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'SIGNIN ERROR'})
#         #return {"status": "SIGNIN ERROR"}
#
#
# @api.post(APIRoutes.acc_refresh_token)
# def check_and_send_new_token(
#                        refresh_token: str,
#                        access_token: OAuth2PasswordBearer = Depends(get_current_user)
#                        ):
#     """CHECK SENDED REFRESH TOKEN AFTER
#        THIS REFRESH ALL TOKENS AND SEND NEW"""
#     if SMa.check_refresh_token(client_refresh_token=refresh_token):
#         return {
#             "access_token": SMa.ACCESS_TOKEN_FOR_CHECK,
#             "refresh_token": SMa.REFRESH_TOKEN_FOR_CHECK
#         }
#     raise HTTPException(status_code=401, detail="ERROR", headers={'status': 'TOKEN UPDATE ERROR'})
#
# # @api.get(APIRoutes.acc_login_route)
# # async def signin_acc_info(access_token: OAuth2PasswordBearer = Depends(create_access_token)):
# #     check_ = SMp.signin_acc(acc_email=acc_sign_model.username, acc_pass=acc_sign_model.password)
# #     if check_[0]:
# #         return {
# #             "access_token": create_access_token(check_[1]),
# #             "refresh_token": create_refresh_token(check_[1]),
# #         }
# #         # return check_[1]
# #     else:
# #         raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'SIGNIN ERROR'})
# """-------------END OF ACCOUNT API-s-----------------"""
#
#
#
#
# """-------------START OF TARIFES API-s-----------------"""
#
#
# @api.get(APIRoutes.get_tarifes_for_view_route)
# def get_tarifes_for_view_route(access_token: OAuth2PasswordBearer = Depends(get_current_user)):
#     """ GET ALL POSSIBLE TARIFES FOR VIEW """
#     temp_ = SMt.get_tarifes_for_view()
#     if temp_[0]:
#         return temp_[1]
#     raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'TARIF VIEW ERROR'})
#
#
# @api.post(APIRoutes.post_tarife_to_client)
# def post_tarife_to_client(tarif_for_client: TarifToClient, access_token: OAuth2PasswordBearer = Depends(get_current_user)):
#     """ POST TARIFE FOR CLIENT """
#     if SMt.post_tarif_to_company(tarif=tarif_for_client):
#         return {"status": "TARIF ADDED TO CLIENT"}
#     raise HTTPException(status_code=404, detail="ERROR", headers={'status': 'TARIF ADD ERROR'})
#
#
# """-------------END OF TARIFES API-s-----------------"""
#
#
# def start_server():
#     """Start server"""
#     run(api)
#
#
# #192.168.3.250
# #'192.168.0.104'
# #192.168.3.203