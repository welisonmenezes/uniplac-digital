import { IS_USER_LOGGEDIN } from '../Actions/ActionTypes';

export const setUserLogginStatus = value => ({
    type: IS_USER_LOGGEDIN,
    payload: value
});
