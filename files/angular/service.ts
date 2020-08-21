import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';

import { ResponseMessage } from '../models/ResponseMessage';
IMPORTS

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
}

@Injectable()
export class %Service {
    URLS

    constructor(private http: HttpClient) { }

    SERVICE_CALLS
}