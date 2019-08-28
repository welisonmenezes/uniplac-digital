import { UsersReducer } from './UsersReducer';
import { combineReducers } from 'redux';

export const Reducers = combineReducers({
  usersState: UsersReducer
});