import React, {FC, useState, useEffect, useReducer} from 'react'
import {Button, Divider} from '@looker/components'
import ProjectsContext from '../context/projects'
import projectsReducer, {IProject} from '../reducers/projects'
import AddProjectModal from './ProjectModal'
import ProjectList from './ProjectList'

export const ProjectsScene: FC<{path: string}> = () => {
  const [projects, dispatch] = useReducer(projectsReducer, [])
  const [isOpen, setModalOpen] = useState(false)

  const handleAddProjectModal = () => {
    setModalOpen(!isOpen)
  }

  useEffect(() => {
    async function fetchProjects() {
      try {
        const projects = await fetch('/projects')
        dispatch({
          type: 'POPULATE_PROJECTS',
          payload: (await projects.json()) as IProject[],
        })
      } catch (e) {
        console.error('Something went wrong', e)
      }
    }
    fetchProjects()
  }, [])

  return (
    <ProjectsContext.Provider value={{projects, dispatch}}>
      <p>
        Below is a list of projects taking place at the hackathon you registered
        for. You can register your project if you haven't already!
      </p>
      <Divider customColor="white" />
      <ProjectList />
      <Button iconBefore="CircleAdd" mr="large" onClick={handleAddProjectModal}>
        Add Project
      </Button>
      <AddProjectModal
        isOpen={isOpen}
        handleModalClose={handleAddProjectModal}
      />
    </ProjectsContext.Provider>
  )
}
