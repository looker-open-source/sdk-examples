import i18n from './i18n'
import {
  Button,
  Box,
  FieldText,
  Heading,
  Paragraph,
  FieldSelect,
  Label,
  ButtonToggle,
  ButtonItem,
  ValidationMessage,
  FieldCheckbox,
  Spinner,
  Flex,
  Divider,
} from '@looker/components'
import {navigate} from '@reach/router'
import {FieldProps, Formik, Form, Field} from 'formik'
import GoogleLogin from 'react-google-login'
import {
  GoogleLoginResponseOffline,
  GoogleLoginResponse,
} from 'react-google-login'
import React from 'react'
import * as yup from 'yup'

const ValidatedFieldCheckbox: React.FC<FieldProps> = ({
  field,
  form: {errors, touched},
  ...props
}) => {
  const error = errors[field.name]
  const touch = touched[field.name]
  return (
    <FieldCheckbox
      validationMessage={
        error && touch
          ? {type: 'error', message: i18n.t('checkboxError', {error})}
          : undefined
      }
      {...field}
      {...props}
    />
  )
}

const ValidatedFieldText: React.FC<FieldProps> = ({
  field,
  form: {errors, touched},
  ...props
}) => {
  const error = errors[field.name]
  const touch = touched[field.name]
  const key =
    error === 'email must be a valid email'
      ? 'textFieldValidationError'
      : 'textFieldMissingError'
  return (
    <FieldText
      validationMessage={
        error && touch
          ? {type: 'error', message: i18n.t(key, {field: `$t(${field.name})`})}
          : undefined
      }
      {...field}
      {...props}
    />
  )
}

const TshirtSize: React.FC<FieldProps> = ({
  field: {onChange, ...field},
  form: {errors, touched},
  ...props
}) => {
  const error = errors[field.name]
  const touch = touched[field.name]
  const handleChange = (value: string) => {
    onChange({target: {value, name: field.name}})
  }
  return (
    <Box mb="large">
      <ButtonToggle onChange={handleChange} {...field}>
        <ButtonItem>XS</ButtonItem>
        <ButtonItem>S</ButtonItem>
        <ButtonItem>M</ButtonItem>
        <ButtonItem>L</ButtonItem>
        <ButtonItem>XL</ButtonItem>
        <ButtonItem>XXL</ButtonItem>
      </ButtonToggle>
      {error && touch && (
        <ValidationMessage
          type="error"
          message={i18n.t('checkboxError', {error})}
        />
      )}
    </Box>
  )
}

const ValidatedFieldSelect: React.FC<FieldProps> = ({
  field,
  form: {errors, touched},
  ...props
}) => {
  const error = errors[field.name]
  const touch = touched[field.name]
  return (
    <FieldSelect
      validationMessage={
        error && touch
          ? {type: 'error', message: i18n.t(error as string)}
          : undefined
      }
      {...field}
      {...props}
    />
  )
}

const HackathonSelect: React.FC<{hackathons: string[]}> = ({hackathons}) => {
  //let options = [{value: '', label: 'Select Hack'}]
  let options = []
  for (let [name, label] of Object.entries(hackathons)) {
    options.push({value: name, label: label})
  }
  return (
    <Field
      placeholder="Select a Hack"
      options={options}
      label="Hackathon"
      component={ValidatedFieldSelect}
      name="hackathon"
    />
  )
}

interface State {
  csrfToken: string
  email: string
  firstName: string
  lastName: string
  hackathons: string[]
  emailVerified: boolean
}

const initialState: State = {
  csrfToken: 'someToken',
  email: '',
  firstName: '',
  lastName: '',
  hackathons: [],
  emailVerified: false,
}

function reducer(
  state: State,
  action: {type: string; payload: Partial<State>}
) {
  switch (action.type) {
    case 'update':
      return {...state, ...action.payload}
    default:
      throw new Error()
  }
}

export const RegisterScene: React.FC<{path: string}> = () => {
  const [
    {csrfToken, email, firstName, lastName, hackathons, emailVerified},
    dispatch,
  ] = React.useReducer(reducer, initialState)

  React.useEffect(() => {
    async function fetchData() {
      try {
        const newHackathons = await fetch('/hackathons')
        dispatch({
          type: 'update',
          payload: {hackathons: await newHackathons.json()},
        })
        const newCsrf = await fetch('/csrf')
        dispatch({
          type: 'update',
          payload: {
            csrfToken: ((await newCsrf.json()) as {token: string}).token,
          },
        })
      } catch (e) {} // TODO: hack for local frontend dev
    }
    fetchData()
  }, [])

  const responseGoogle = React.useCallback(
    (response: GoogleLoginResponseOffline | GoogleLoginResponse) => {
      async function handleGoogleResponse() {
        try {
          const result = await fetch('/verify_google_token', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(response),
          })
          if (result.ok) {
            const msg = await result.json()
            dispatch({
              type: 'update',
              payload: {
                firstName: msg.given_name,
                lastName: msg.family_name,
                email: msg.email,
                emailVerified: true,
              },
            })
          } else {
            console.log(result)
          }
        } catch (e) {
          alert(JSON.stringify(response, null, 2))
        }
      }
      handleGoogleResponse()
    },
    []
  )

  return (
    <>
      <Heading as="h1">{i18n.t('Hackathon Registration')}</Heading>
      <Paragraph>{i18n.t('Register for a Hackathon below')}</Paragraph>
      <Divider my="large" />
      <Heading mb="medium">{i18n.t('Registration')}</Heading>
      <GoogleLogin
        clientId="280777447286-iigstshu4o2tnkp5fjucrd3nvq03g5hs.apps.googleusercontent.com"
        onSuccess={responseGoogle}
        onFailure={responseGoogle}
        cookiePolicy={'single_host_origin'}
      />
      <Divider my="large" />
      <Formik
        enableReinitialize // for csrf token
        initialValues={{
          csrf_token: csrfToken,
          first_name: firstName,
          last_name: lastName,
          email: email,
          organization: '',
          role: '',
          hackathon: '',
          tshirt_size: '',
          ndaq: false,
          code_of_conduct: false,
          contributing: false,
          email_verified: emailVerified,
        }}
        validationSchema={() =>
          yup.object().shape({
            csrf_token: yup.string().required(),
            email_verified: yup.boolean(),
            first_name: yup.string().required(),
            last_name: yup.string().required(),
            email: yup
              .string()
              .email()
              .required(),
            organization: yup.string().required(),
            role: yup.string().required(),
            hackathon: yup.string().required(),
            tshirt_size: yup
              .string()
              .oneOf(['XS', 'S', 'M', 'L', 'XL', 'XXL'])
              .required(),
            ndaq: yup
              .boolean()
              .oneOf([true], 'Required')
              .required(),
            code_of_conduct: yup
              .boolean()
              .oneOf([true], 'Required')
              .required(),
            contributing: yup
              .boolean()
              .oneOf([true], 'Required')
              .required(),
          })
        }
        onSubmit={(values, actions) => {
          async function fetchData() {
            try {
              const result = await fetch('/register', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(values),
              })
              const msg = await result.json()
              if (msg.ok) {
                navigate('/thankyou')
              } else {
                actions.setStatus(msg.message)
                actions.setSubmitting(false)
              }
            } catch (e) {
              // TODO: hack for local frontend dev
              alert(JSON.stringify(values, null, 2))
              actions.setSubmitting(false)
            }
          }
          fetchData()
        }}
      >
        {({isSubmitting, status, errors, values, touched}) => {
          return (
            <Form>
              <Field type="hidden" name="csrf_token" value={csrfToken} />
              <Field
                label={i18n.t('First Name')}
                component={ValidatedFieldText}
                name="first_name"
                placeholder={i18n.t('First Name')}
              />
              <Field
                label={i18n.t('Last Name')}
                component={ValidatedFieldText}
                name="last_name"
                placeholder={i18n.t('Last Name')}
              />
              <Field
                label={i18n.t('Email')}
                component={ValidatedFieldText}
                name="email"
                placeholder={i18n.t('Email Address')}
              />
              <Field
                label={i18n.t('Organization')}
                component={ValidatedFieldText}
                name="organization"
                placeholder={i18n.t('Organization')}
              />
              <Field
                label={i18n.t('Role')}
                component={ValidatedFieldText}
                name="role"
                placeholder={i18n.t('Role')}
              />
              <HackathonSelect hackathons={hackathons} />
              <Label>{i18n.t('T-Shirt Size')}</Label>
              <Field name="tshirt_size" component={TshirtSize} />
              <Field
                name="ndaq"
                type="checkbox"
                label={i18n.t('I agree to the Terms and Conditions/NDAQ')}
                alignLabel="right"
                labelWidth="auto"
                component={ValidatedFieldCheckbox}
                branded
              />
              <Field
                name="code_of_conduct"
                type="checkbox"
                label={i18n.t('I agree to the Code of Conduct')}
                alignLabel="right"
                labelWidth="auto"
                component={ValidatedFieldCheckbox}
                branded
              />
              <Field
                name="contributing"
                type="checkbox"
                label={i18n.t('I agree to the Contribution Guidelines')}
                alignLabel="right"
                labelWidth="auto"
                component={ValidatedFieldCheckbox}
                branded
              />
              <Field
                name="email_verified"
                type="hidden"
                value={emailVerified}
              />
              {status && <div>{status}</div>}
              <Flex alignItems="center" mt="medium">
                {isSubmitting && <Spinner mr="small" />}
                <Button disabled={isSubmitting}>{i18n.t('Register')}</Button>
              </Flex>
            </Form>
          )
        }}
      </Formik>
    </>
  )
}
