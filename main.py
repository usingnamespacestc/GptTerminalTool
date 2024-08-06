from openai import OpenAI
import argparse
import subprocess


def send_independent_request(content="Say this is a test"):
    client = OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )
    result = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            result += chunk.choices[0].delta.content
    return result


def run_command(command):
    new_command = "cmd /k " + command + " & pause"
    subprocess.run(['start', 'cmd', '/c', new_command], shell=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', '-e', type=str, help='Execute the command required')
    parser.add_argument('--code', '-c', type=str, help='Help me write the code I want')
    parser.add_argument('--ask', '-a', type=str, help='Ask a question')
    args = parser.parse_args()
    if args.execute is not None:
        message = "请帮我生成windows命令行命令，只返回给我该命令不要说任何多余的话，连上面的“bash”和引号都不要有。之后我会把你发给我的命令直接发送到命令行中运行：" + args.execute
        command = send_independent_request(message)

        print("\nExecute it now? [Y/N]")
        answer = input().replace(" ", "")
        if answer == "Y" or answer == "y":
            run_command(command)
        else:
            print("Cancel")
    if args.code is not None:
        message = "请帮我写一下这个代码，只返回给我单段代码不要说任何其他多余的话：" + args.code
        send_independent_request(message)
    if args.ask is not None:
        message = args.ask
        send_independent_request(message)
    pass


if __name__ == "__main__":
    main()
