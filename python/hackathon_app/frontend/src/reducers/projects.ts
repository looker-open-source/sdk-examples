export interface IProject {
  id: string
  registration_id: string
  title: string
  description: string
  date_created: Date
  project_type: string
  contestant: boolean
  locked: boolean
}

export interface ProjectAction {
  type: string
  payload: IProject[]
}

const projectsReducer = (
  state: IProject[],
  action: ProjectAction
): IProject[] => {
  const firstProject = action.payload[0]
  switch (action.type) {
    case 'POPULATE_PROJECTS':
      return action.payload
    case 'ADD_PROJECT':
      return [...state, firstProject]
    case 'EDIT_PROJECT':
      return state.map(project => {
        if (project.id === firstProject.id) {
          return {
            ...project,
            ...firstProject,
          }
        } else {
          return project
        }
      })
    case 'REMOVE_PROJECT':
      return state.filter(project => project.id !== firstProject.id)
    default:
      return state
  }
}

export {projectsReducer as default}
