export class ResponseMessage {

    constructor(
        private message: string
    ){}

    public get_message(): string {
		return this.message;
	}
}