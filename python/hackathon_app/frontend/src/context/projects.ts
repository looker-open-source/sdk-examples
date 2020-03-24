import noop from 'lodash/noop'
import React, {Dispatch} from 'react'
import {IProject, ProjectAction} from '../reducers/projects'

export interface ProjectContextProps {
  projects: IProject[]
  dispatch: Dispatch<ProjectAction>
}

const initialObject: ProjectContextProps = {
  projects: [],
  dispatch: noop,
}

const ProjectsContext = React.createContext(initialObject)

export {ProjectsContext as default}
