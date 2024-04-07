import { faker } from '@faker-js/faker'

describe('Todo Tests', () => {
  const test_username = faker.internet.userName();
  const test_password = faker.internet.password();

  const test_title = faker.lorem.words(4);
  const test_description = faker.lorem.words(10);

  //Before all tests once
  before(() => {
    // Intercept the create user request
    cy.intercept('POST', '/api/user/create_user').as('createUserRequest');

    cy.visit('http://localhost')
    //Register a user
    cy.get('a[href="/register"]').click()
    cy.get('input[name="username"]').type(test_username)
    cy.get('input[name="password"]').type(test_password)
    cy.get('button[type="submit"]').click()

    // Wait for the login request to complete
    cy.wait('@createUserRequest').then((interception) => {
      //201 for create user or 400 for user already exists
      expect(interception.response.statusCode).to.be.oneOf([201, 400])
    })
  })

  //Before each test
  beforeEach(() => {
    //Preserve the session
    cy.session('userSession', () => {
      //Intercept the login request
      cy.intercept('POST', '/api/user/login').as('loginRequest');
      cy.visit('http://localhost')
      //Login the user
      cy.get('input[name="username"]').type(test_username)
      cy.get('input[name="password"]').type(test_password)
      cy.get('button[type="submit"]').click()
      //Wait for the login request to complete
      cy.wait('@loginRequest').then((interception) => {
        expect(interception.response.statusCode).to.eq(200)
      })
    })
    cy.visit('http://localhost')
  })

  it('creates a todo', () => {
    //Intercept the create todo request
    cy.intercept('POST', '/api/todo/create_todo').as('createTodoRequest');

    cy.get('input[placeholder="Title"]').type(test_title)
    cy.get('input[placeholder="Description"]').type(test_description)
    cy.get('button[type="submit"]').click()

    //Wait for the create todo request to complete
    cy.wait('@createTodoRequest').then((interception) => {
      expect(interception.response.statusCode).to.eq(201)
    })

    //Assert the todo was created
    cy.contains("h3", test_title)
    cy.contains("p", test_description)
    cy.get(`input[data-testid='completed-${test_title}']`).should('not.be.checked')
  })

  it('completes a todo', () => {
    cy.contains("h3", test_title)
    cy.get(`input[data-testid="completed-${test_title}"]`).click()
    cy.get(`input[data-testid='completed-${test_title}']`).should('be.checked')
  })

  it('deletes a todo', () => {
    cy.get(`[data-testid="delete-${test_title}"]`).click()
    cy.contains('h3', test_title).should('not.exist')
  })
})