import React, {useState} from 'react'
import {isEqual} from 'lodash'
import {
  Dialog,
  ConfirmLayout,
  Box,
  Icon,
  Heading,
  FieldText,
  Button,
  ButtonTransparent,
} from '@looker/components'

interface IProps {
  isOpen: boolean
  handleModalClose: CallableFunction
  title: string
}

const ProjectModal: React.FC<IProps> = ({isOpen, handleModalClose, title}) => {
  /**
   * Track form input state, and create helper function to compare updated state to default state
   */
  const defaultFormData = {
    title: '',
    description: '',
    type: '',
    contestant: '',
  }
  const [formData, setFormData] = useState(defaultFormData)

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
  const [isCancellingInput, setIsCancellingInput] = useState(false)

  /**
   * Create callbacks for the various actions:
   * - save
   * - cancel
   * - confirm close (e.g. "Yes I want to discard my changes and close the dialog")
   * - reset form (e.g. "Don't close, let me continue editing")
   */

  const handleSave = () => {
    alert('Saved!') // dispatch side effect
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
          title={title}
          message={
            <form>
              <FieldText
                name="title"
                label="Title"
                onChange={handleInputChange}
                value={formData.title}
              />
              <FieldText
                name="description"
                label="Description"
                onChange={handleInputChange}
                value={formData.description}
              />
              <FieldText
                name="type"
                label="Type"
                onChange={handleInputChange}
                value={formData.type}
              />
              <FieldText
                name="contestant"
                label="Contestant"
                onChange={handleInputChange}
                value={formData.contestant}
              />
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
