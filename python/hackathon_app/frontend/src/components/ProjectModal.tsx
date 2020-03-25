import React, {useState, useEffect, useContext} from 'react'
import {isEqual} from 'lodash'
import {
  Dialog,
  ConfirmLayout,
  Icon,
  FieldText,
  Divider,
  ButtonToggle,
  ButtonItem,
  Text,
  ToggleSwitch,
  Label,
  Button,
  ButtonTransparent,
  FieldTextArea,
} from '@looker/components'
import {IProject} from '../reducers/projects'
import ProjectsContext from '../context/projects'

interface IProps {
  isOpen: boolean
  handleModalClose: CallableFunction
  project?: IProject
}

const ProjectModal: React.FC<IProps> = ({
  isOpen,
  handleModalClose,
  project,
}) => {
  const {dispatch} = useContext(ProjectsContext)

  /**
   * Track form input state, and create helper function to compare updated state to default state
   */
  let defaultFormData = {
    title: '',
    description: '',
    type: '',
    contestant: '',
  }
  const [formData, setFormData] = useState(defaultFormData)
  const [isCancellingInput, setIsCancellingInput] = useState(false)

  const [isContestant, setIsContestant] = useState(
    project ? project.contestant : true
  )

  const [projectType, setProjectType] = useState(
    project ? project.project_type : 'Open'
  )

  useEffect(() => {
    defaultFormData = {
      title: project ? project.title : '',
      description: project ? project.description : '',
      type: project ? project.project_type : '',
      contestant: project ? project.contestant.toString() : '',
    }
    setProjectType(project ? project.project_type : 'Open')
    setIsContestant(project ? project.contestant : true)
    setFormData(defaultFormData)
  }, [isOpen])

  const hasUnsavedChanges = () => {
    if (isEqual(formData, defaultFormData)) {
      return false
    } else {
      return true
    }
  }

  const handleInputChange = (e: any) => {
    const {name, value} = e.target
    setFormData({...formData, [name]: value})
  }

  /**
   * Track dialog state: open, close, or cancelling input
   */

  const handleSave = () => {
    dispatch({
      type: project ? 'EDIT_PROJECT' : 'ADD_PROJECT',
      payload: [
        {
          // TODO: this will change when backend endpoints are in place
          ...formData,
          id: project ? project.id : '100',
          registration_id: '100',
          date_created: new Date(),
          project_type: 'Invite Only',
          locked: false,
          contestant: false,
        },
      ],
    })
    handleModalClose() // close dialog
    setFormData(defaultFormData) // reset form state
  }

  const handleCancel = () => {
    if (hasUnsavedChanges()) {
      // has unsaved changes: keep dialog open and update state to reflect attempt at closing the form
      setIsCancellingInput(true)
    } else {
      // no unsaved changes: close the dialog
      handleModalClose()
    }
  }

  const handleConfirmClose = () => {
    // "Yes I want to discard my changes and close the dialog"
    handleModalClose() // close form
    setIsCancellingInput(false) // reset modal state
    setFormData(defaultFormData) // reset form state
  }

  const handleDialogReset = () => {
    setIsCancellingInput(false) // take me back to dialog #1
  }

  /**
   * Render the two dialogs and associated content
   */
  return (
    <>
      {/*
          Dialog #1: User information input
        */}
      <Dialog
        isOpen={isOpen && !isCancellingInput}
        onClose={handleCancel}
        width="500px"
      >
        <ConfirmLayout
          title="Enter project details below"
          message={
            <form>
              <FieldText
                name="title"
                label="Title"
                onChange={handleInputChange}
                value={formData.title}
              />
              <FieldTextArea
                name="description"
                label="Description"
                onChange={handleInputChange}
                value={formData.description}
              />

              <Text fontSize="small">Type</Text>
              <Divider customColor="white" />
              <ButtonToggle value={projectType} onChange={setProjectType}>
                <ButtonItem>Open</ButtonItem>
                <ButtonItem>Invite Only</ButtonItem>
                <ButtonItem>Closed</ButtonItem>
                <ButtonItem>Yuri</ButtonItem>
              </ButtonToggle>

              <Divider customColor="white" />

              <Label htmlFor="switch">
                Locked
                <ToggleSwitch
                  onChange={() => setIsContestant(!isContestant)}
                  on={isContestant}
                  id="switch"
                />
              </Label>
            </form>
          }
          primaryButton={<Button onClick={handleSave}>Save</Button>}
          secondaryButton={
            <ButtonTransparent onClick={handleCancel}>Cancel</ButtonTransparent>
          }
        />
      </Dialog>

      {/* Dialog #2: fallback "discard changes" dialog */}
      <Dialog
        isOpen={isOpen && isCancellingInput}
        onClose={handleConfirmClose}
        width="500px"
      >
        <ConfirmLayout
          title="Discard Changes?"
          titleIcon={<Icon name="Warning" color="palette.red500" size={22} />}
          message="Are you sure you want to close the dialog? Unsaved changes will be lost."
          primaryButton={
            <ButtonTransparent onClick={handleConfirmClose} color="danger">
              Discard Changes
            </ButtonTransparent>
          }
          secondaryButton={
            <ButtonTransparent onClick={handleDialogReset} color="neutral">
              Go Back
            </ButtonTransparent>
          }
        />
      </Dialog>
    </>
  )
}

export {ProjectModal as default}
