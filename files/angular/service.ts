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
export class _TBL_NM_Service {
    URLS

    constructor(private http: HttpClient) { }

	getAll_TBL_NM_(): Observable<_TBL_NM_DTO[]> {
		return this.http.get<_TBL_NM_DTO[]>(this.getAll_TBL_NM_URL);
	}
	find_TBL_NM_ById(id: number): Observable<_TBL_NM_DTO> {
		let find_TBL_NM_ByIdURL_temp = this.find_TBL_NM_ByIdURL.replace("{id}",id.toString(10));
		return this.http.get<_TBL_NM_DTO>(find_TBL_NM_ByIdURL_temp);
	}
	create_TBL_NM_(data: _TBL_NM_DTO): Observable<_TBL_NM_DTO> {
		return this.http.post<_TBL_NM_DTO>(this.create_TBL_NM_URL, data, httpOptions);
	}
	update_TBL_NM_(data: _TBL_NM_DTO): Observable<_TBL_NM_DTO> {
		return this.http.post<_TBL_NM_DTO>(this.update_TBL_NM_URL, data, httpOptions);
	}
	delete_TBL_NM_(id: number): Observable<ResponseMessage> {
		let delete_TBL_NM_URL_temp = this.delete_TBL_NM_URL.replace("{id}",id.toString(10));
		return this.http.delete<ResponseMessage>(delete_TBL_NM_URL_temp, httpOptions);
	}

	FK_SECTION
}