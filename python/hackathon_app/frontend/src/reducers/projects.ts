import moment from 'moment'

export interface IProject {
  id: string
  registrationId: string
  title: string
  description: string
  dateCreated: moment.Moment
  projectType: string
  contestant: boolean
  locked: boolean
}

const projectsReducer = (
  state: IProject[],
  action: {type: string; payload: Partial<IProject>}
) => {
  switch (action.type) {
    case 'ADD_PROJECT':
      return [...state, action.payload]
    case 'EDIT_PROJECT':
      return state.map(project => {
        if (project.id === action.payload.id) {
          return {
            ...project,
            ...action.payload,
          }
        } else {
          return project
        }
      })
    case 'REMOVE_PROJECT':
      return state.filter(project => project.id !== action.payload.id)
    default:
      return state
  }
}

export {projectsReducer as default}
