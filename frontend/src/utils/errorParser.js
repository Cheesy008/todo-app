export default (errors) => {
    return errors.response.data['errors'].map(el => el.message)
}