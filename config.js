const env = process.env.NODE_ENV || 'production'

//insert your API Key & Secret for each environment, keep this file local and never push it to a public repo for security purposes.
const config = {
	development :{
		APIKey : '',
		APISecret : ''
	},
	production:{	
		APIKey : 'SQu_b5ZnQ2qQPZNQolFzCg',
		APISecret : 'hlwiCI3h9vIR4UiIJJxw8X8ebQTmWwj6YefT'
	}
};

module.exports = config[env]
