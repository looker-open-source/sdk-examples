import React, {Dispatch} from 'react'
import {IProject} from '../reducers/projects'

const initialObject: {
  projects: IProject[]
  dispatch: React.Dispatch<{action: string; payload: IProject[]}>
} = {
  projects: [],
  dispatch: '',
}

const ProjectsContext = React.createContext(initialObject)

export {ProjectsContext as default}
