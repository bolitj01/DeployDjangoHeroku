import { faker } from '@faker-js/faker'

describe('User Tests', () => {
  const test_username = faker.internet.userName();
  const test_password = faker.internet.password();

  // Go to localhost before each test
  beforeEach(() => {
    cy.visit('http://localhost')
  })

  it('user register', () => {
    //Intercept the user register request
    cy.intercept('POST', '/api/user/create_user').as('createUserRequest');
    cy.get('a[href="/register"]').click()
    cy.get('input[name="username"]').type(test_username)
    cy.get('input[name="password"]').type(test_password)
    cy.get('button[type="submit"]').click()
    //Verify request
    cy.wait('@createUserRequest').then((interception) => {
      expect(interception.response.statusCode).to.be.oneOf([201, 400])
    })
  })

  it('user login', () => {
    //Intercept the user login request
    cy.intercept('POST', '/api/user/login').as('loginRequest');
    cy.get('input[name="username"]').type(test_username)
    cy.get('input[name="password"]').type(test_password)
    cy.get('button[type="submit"]').click()
    //Verify request
    cy.wait('@loginRequest').then((interception) => {
      expect(interception.response.statusCode).to.eq(200)
    })
    cy.visit('http://localhost')
    cy.contains("Todo List")
  })

  it ('user logout', () => {
    //Intercept the user login and logout request
    cy.intercept('POST', '/api/user/logout').as('logoutRequest');
    cy.intercept('POST', '/api/user/login').as('loginRequest');
    //Login first
    cy.get('input[name="username"]').type(test_username)
    cy.get('input[name="password"]').type(test_password)
    cy.get('button[type="submit"]').click()
    //Verify login request
    cy.wait('@loginRequest').then((interception) => {
      expect(interception.response.statusCode).to.eq(200)
    })
    //Intercept home page request
    cy.intercept('GET', '/').as('homeRequest');
    cy.visit('http://localhost')
    cy.wait('@homeRequest')
    cy.get('button[data-testid="logout"]').click()
    //Check Login text present
    cy.contains('Login')
  })
})
