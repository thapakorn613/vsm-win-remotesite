const env = process.env.NODE_ENV || 'production'

//insert your API Key & Secret for each environment, keep this file local and never push it to a public repo for security purposes.
const config = {
	development :{
		APIKey : '',
		APISecret : ''
	},
	production:{	
		APIKey : 'nDvEhZf6T8C-o-gAzehRCA',
		APISecret : 'KupluxPdGOynxWZwD7t9qV10taxRv6RZFakE'
	}
};

module.exports = config[env]