import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';

import { ResponseMessage } from '../models/ResponseMessage';
XXX

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
}

@Injectable()
export class %Service {
    ZZZ

    constructor(private http: HttpClient) { }

    YYY
}