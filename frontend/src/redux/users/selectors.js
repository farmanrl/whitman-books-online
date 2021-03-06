import { createSelector } from 'reselect';

const getUserList = state => state.usersReducer.userList;

const getUserId = (state, props) => props.userId;

export const getUserById = createSelector(
  [getUserList, getUserId],
  (userList, userId) => {
    const user = userList.find(item => item.googleId === userId);
    return user;
  },
);
