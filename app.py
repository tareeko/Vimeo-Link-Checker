from tkinter import *
import vimeo
from pprint import pprint

v = vimeo.VimeoClient(
    token=[ACCESS_TOKEN],
    key=[KEY],
    secret=[SECRET]
)

root = Tk()
root.geometry("500x590")
root.title("Vimeo Link Checker")


def process_input():
    user_input = input_text.get("1.0", END)
    links = user_input.split('\n')
    links_status = []
    final_string = ""
    # print(links[0])
    # print(links[0].split('m/')[1])
    print(user_input)
    output.delete("1.0", END)
    for link in links:
        print(f'Link is {link}')
        try:
            video_id = link.split('m/')[1]
            response = v.get(f'https://api.vimeo.com/videos/{video_id}')
            response_json = response.json()
            # print(response.status_code)
            if response.status_code == 404:
                # print("video not found")
                final_string += f"{link}\tVideo Not Found\n"
            else:
                try:
                    # print("trying")
                    if response_json['invalid_parameters'][0]['field'] == 'password':
                        final_string += f"{link}\tPrivate Video\n"
                except KeyError:
                    # print('exception')
                    final_string += f'{link}\t{response_json["name"]}\n'
        except IndexError:
            final_string += '\n'
    final_string += "\n\n\nYou can paste these results to a spreadsheet!"
    main_button.config(text="Check More Links")
    show_output(final_string)


def show_output(output_text):
    output.delete("1.0", END)
    output.insert(END, output_text)


user_prompt = Label(text="Paste Vimeo links here:")
credit = Label(text="Made for SSE with ♥ by Tarek Alward")
input_text = Text(root, height=15,
                  width=55,
                  bg="light yellow")

output = Text(root, height=15,
              width=55,
              bg="light cyan")

main_button = Button(root, height=2,
                     width=20,
                     text="Check Links",
                     command=process_input)

user_prompt.pack()
input_text.pack()
main_button.pack()
output.pack()
credit.pack()

mainloop()
