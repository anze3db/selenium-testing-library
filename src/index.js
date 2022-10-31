import { queryAllByText, queryAllByRole, queryAllByPlaceholderText, queryAllByLabelText, queryAllByAltText, queryAllByTitle, queryAllByTestId, queryAllByDisplayValue } from '@testing-library/dom'

window.__stl__ = {}
window.__stl__.queryAllByText = queryAllByText
window.__stl__.queryAllByRole = queryAllByRole
window.__stl__.queryAllByPlaceholderText = queryAllByPlaceholderText
window.__stl__.queryAllByLabelText = queryAllByLabelText
window.__stl__.queryAllByAltText = queryAllByAltText
window.__stl__.queryAllByTitle = queryAllByTitle
window.__stl__.queryAllByTestId = queryAllByTestId
window.__stl__.queryAllByDisplayValue = queryAllByDisplayValue
