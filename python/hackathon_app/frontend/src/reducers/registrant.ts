interface State {
  csrfToken: string
  email: string
  firstName: string
  lastName: string
  hackathons: string[]
  emailVerified: boolean
}

const initialState: State = {
  csrfToken: 'someToken',
  email: '',
  firstName: '',
  lastName: '',
  hackathons: [],
  emailVerified: false,
}

function reducer(
  state: State = initialState,
  action: {type: string; payload: Partial<State>}
) {
  switch (action.type) {
    case 'update':
      return {...state, ...action.payload}
    default:
      throw new Error()
  }
}

export {reducer as default}
