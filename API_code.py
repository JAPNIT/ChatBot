from api.ai import Agent
import json


#initialize the agent 
agent = Agent(
     'sakd',
     '04f67374d4b14ed68d9f13f70ddfdca8',
     '7b62bcd174784e09ab76acc96be378ed',
)

# actions defined in the API.AI console that fire locally when an intent is
# recognized
def medical_records(medical):
        print ('bweh')
	
def saveColor(color):
	print ('do something here')

def createOrder(address):
	print ('do something here')

def main():
	user_input = ''

	#loop the queries to API.AI so we can have a conversation client-side
	while user_input != 'exit':

		#parse the user input
		user_input  = input("me: ")
		#query the console with the user input, retrieve the response
		response = agent.query(user_input)
		#parse the response
		result = response['result']
		fulfillment = result['fulfillment']

		#if an action is deteted, fire the appropriate function
		if result['action'] == 'medical_records':
                        print(Flag)
                        medical_records(user_input)
		if result['action'] == 'saveColor':
			saveColor(user_input)
		if result['action'] == 'createOrder':
			createOrder(user_input)
		
		print('bot: ' + fulfillment['speech'])


if __name__ == "__main__":
    main()
