import React, {FC, useState, useContext} from 'react'
import {
  useConfirm,
  Button,
  Confirm,
  ActionList,
  ActionListHeaderColumn,
  ActionListColumns,
  ActionListItem,
  ActionListItemColumn,
  ActionListItemAction,
} from '@looker/components'
import ProjectEditModal from './ProjectModal'
import ProjectsContext from '../context/projects'
import {IProject} from '../reducers/projects'

const header = (
  <>
    <ActionListHeaderColumn id="title">Title</ActionListHeaderColumn>
    <ActionListHeaderColumn id="description">
      Description
    </ActionListHeaderColumn>
    <ActionListHeaderColumn id="type">Type</ActionListHeaderColumn>
    <ActionListHeaderColumn id="contestant">Contestant</ActionListHeaderColumn>
  </>
)

const columns: ActionListColumns = [
  {
    title: 'Title',
    id: 'title',
    primaryKey: true,
    type: 'string',
    widthPercent: 30,
  },
  {
    title: 'Description',
    id: 'description',
    primaryKey: false,
    type: 'string',
    widthPercent: 45,
  },
  {
    title: 'projectType',
    id: 'projectType',
    primaryKey: false,
    type: 'string',
    widthPercent: 10,
  },
  {
    title: 'Contestant',
    id: 'contestant',
    primaryKey: false,
    type: 'string',
    widthPercent: 7,
  },
]

const ProjectList: FC = () => {
  let {projects, dispatch} = useContext(ProjectsContext)
  const [isOpen, setModalOpen] = useState(false)
  const [selectedProject, setSelectedProject] = useState(projects[0])

  const handleConfirm = (close: () => void) => {
    dispatch({
      type: 'REMOVE_PROJECT',
      payload: [selectedProject],
    })
    close()
  }

  const [confirmationDialog, openDialog] = useConfirm({
    buttonColor: 'danger',
    confirmLabel: 'Yes, delete',
    message: `Are you sure you want to delete project?`,
    onConfirm: handleConfirm,
    title: `Delete Project`,
  })

  const handleEditProjectModal = (project: IProject) => {
    setSelectedProject(project)
    setModalOpen(!isOpen)
  }

  const items = projects.map(project => (
    <ActionListItem
      key={project.id}
      actions={
        <>
          <ActionListItemAction
            icon="Edit"
            onClick={() => {
              handleEditProjectModal(project)
            }}
          >
            Edit
          </ActionListItemAction>
          <ActionListItemAction
            icon="Trash"
            onClick={() => {
              setSelectedProject(project)
              openDialog()
            }}
          >
            Delete
          </ActionListItemAction>
          <ActionListItemAction
            icon="Favorite"
            onClick={() => console.log('You just voted!')}
          >
            Vote Favorite
          </ActionListItemAction>
        </>
      }
    >
      <ActionListItemColumn>{project.title}</ActionListItemColumn>
      <ActionListItemColumn>{project.description}</ActionListItemColumn>
      <ActionListItemColumn>{project.project_type}</ActionListItemColumn>
      <ActionListItemColumn>
        {project.contestant ? 'Yes' : 'No'}
      </ActionListItemColumn>
    </ActionListItem>
  ))

  return (
    <>
      <ActionList header={header} columns={columns}>
        {items}
      </ActionList>
      <ProjectEditModal
        isOpen={isOpen}
        handleModalClose={handleEditProjectModal}
        project={selectedProject}
      />
      {confirmationDialog}
    </>
  )
}

export {ProjectList as default}
