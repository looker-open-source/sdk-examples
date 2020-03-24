import React, {FC, useState, useEffect, useReducer} from 'react'
import {Button} from '@looker/components'
import ProjectsContext from '../context/projects'
// import projectsReducer from '../reducers/projects'
import ProjectModal from './ProjectModal'
import ProjectList from './ProjectList'

export const ProjectsScene: FC<{path: string}> = () => {
  // const [projects, dispatch] = useReducer(projectsReducer, fakeData)

  // useEffect(() => {
  //   async function fetchProjects() {
  //     try {
  //       const projects = await fetch('/projects')
  //       dispatch({
  //         type: 'POPULATE_PROJECTS',
  //         payload: projects,
  //       })
  //     } catch (e) {
  //       console.error('Something went wrong', e)
  //     }
  //   }
  //   fetchProjects()
  // }, [])

  return (
    // <ProjectsContext.Provider value={projects}>
    <p>This is the projects board</p>
    // <ProjectList />
    // <Button
    //   iconBefore="CircleAdd"
    //   mr="large"
    //   onClick={() => console.log(projects)}
    // >
    //   Add Project
    // </Button>
    // </ProjectsContext.Provider>
  )
}
