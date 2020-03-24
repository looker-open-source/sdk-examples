import React, {FC, useState} from 'react'
import {
  ActionList,
  ActionListHeaderColumn,
  ActionListColumns,
  ActionListItem,
  ActionListItemColumn,
  ActionListItemAction,
} from '@looker/components'
import ProjectModal from './ProjectModal'

const data = [
  {
    projectId: 1,
    title: 'Python SDK',
    description: 'A strongly typed SDK for the Looker API',
    projectType: 'Open',
  },
  {
    projectId: 2,
    title: 'TypeScript SDK',
    description: 'A strongly typed SDK for the Looker API',
    projectType: 'Open',
    contestant: 'Yes',
  },
]

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
    widthPercent: 25,
  },
  {
    title: 'Description',
    id: 'description',
    primaryKey: false,
    type: 'string',
    widthPercent: 25,
  },
  {
    title: 'projectType',
    id: 'projectType',
    primaryKey: false,
    type: 'string',
    widthPercent: 25,
  },
  {
    title: 'Contestant',
    id: 'contestant',
    primaryKey: false,
    type: 'string',
    widthPercent: 25,
  },
]

const ProjectList: FC = () => {
  const [isModalOpen, setModalOpen] = useState(false)
  const [modalTitle, setModalTitle] = useState('')

  const handleModalOpen = (title: string) => {
    setModalTitle(title)
    setModalOpen(true)
  }

  const handleModalClose = () => {
    setModalOpen(false)
  }

  const items = data.map(
    ({projectId, title, description, projectType, contestant}) => (
      <ActionListItem
        key={projectId}
        actions={
          <>
            <ActionListItemAction
              onClick={() => handleModalOpen('Edit project details')}
            >
              Edit
            </ActionListItemAction>
          </>
        }
      >
        <ActionListItemColumn>{title}</ActionListItemColumn>
        <ActionListItemColumn>{description}</ActionListItemColumn>
        <ActionListItemColumn>{projectType}</ActionListItemColumn>
        <ActionListItemColumn>{contestant}</ActionListItemColumn>
      </ActionListItem>
    )
  )

  return (
    <>
      <ActionList header={header} columns={columns}>
        {items}
      </ActionList>
      <ProjectModal
        isOpen={isModalOpen}
        handleModalClose={handleModalClose}
        title={modalTitle}
      />
    </>
  )
}

export {ProjectList as default}
