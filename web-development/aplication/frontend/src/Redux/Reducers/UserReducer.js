import { IS_USER_LOGGEDIN } from '../Actions/ActionTypes';

// utils/extras
import IsLoggedIn from '../../Utils/IsLoggedIn';

const initialState = {
    isUserLoggedin: IsLoggedIn()
};

export const UserReducer = (state = initialState, action) => {
    switch (action.type) {
        case IS_USER_LOGGEDIN:
            return {
                ...state,
                isUserLoggedin: action.payload
            };
        default:
            return state;
    }
};