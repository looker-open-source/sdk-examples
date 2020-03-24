import projectsReducer, {IProject} from '../../reducers/projects'
import projects from '../fixtures/projects'

it('should add a project', () => {
  const state = projectsReducer([], {
    type: 'ADD_PROJECT',
    payload: projects[0],
  })
  expect(state).toEqual([projects[0]])
})

it('should remove a project with a valid id', () => {
  const action = {
    type: 'REMOVE_PROJECT',
    payload: {
      id: projects[1].id,
    },
  }
  const state = projectsReducer(projects, action)
  expect(state).toEqual([projects[0], projects[2]])
})

it('should remove a project with a invalid id', () => {
  const action = {
    type: 'REMOVE_PROJECT',
    payload: {
      id: '-1',
    },
  }
  const state = projectsReducer(projects, action)
  expect(state).toEqual(projects)
})

it('should edit a project with a valid id', () => {
  const action = {
    type: 'EDIT_PROJECT',
    payload: {
      id: projects[1].id,
      title: 'A new title',
      description: 'And a brand new description',
    },
  }
  const state = projectsReducer(projects, action)
  expect(state).toEqual([
    projects[0],
    {
      ...projects[1],
      title: action.payload.title,
      description: action.payload.description,
    },
    projects[2],
  ])
})
