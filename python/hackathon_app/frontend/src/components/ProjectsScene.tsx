import React, {FC, useState} from 'react'
import {
  ActionList,
  ActionListHeaderColumn,
  ActionListColumns,
  ActionListItem,
  ActionListItemColumn,
  ActionListItemAction,
} from '@looker/components'
import {Modal} from './EditModal'

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
    <ActionListHeaderColumn>Title</ActionListHeaderColumn>
    <ActionListHeaderColumn>Description</ActionListHeaderColumn>
    <ActionListHeaderColumn>Type</ActionListHeaderColumn>
    <ActionListHeaderColumn>Contestant</ActionListHeaderColumn>
  </>
)

const columns: ActionListColumns = [
  {
    children: 'Title',
    id: 'title',
    primaryKey: true,
    type: 'string',
    widthPercent: 25,
  },
  {
    children: 'Description',
    id: 'description',
    primaryKey: false,
    type: 'string',
    widthPercent: 25,
  },
  {
    children: 'projectType',
    id: 'projectType',
    primaryKey: false,
    type: 'string',
    widthPercent: 25,
  },
  {
    children: 'Contestant',
    id: 'contestant',
    primaryKey: false,
    type: 'string',
    widthPercent: 25,
  },
]

const EditableGrid: FC<{path: string}> = () => {
  const [isModalOpen, setModalOpen] = useState(false)

  const handleModalOpen = () => {
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
            <ActionListItemAction onClick={handleModalOpen}>
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
      <Modal isOpen={isModalOpen} handleModalClose={handleModalClose} />
    </>
  )
}

export {EditableGrid}
