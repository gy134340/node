/**
 * my node spider
 * @author  gy
 */

var request = require('superagent');
var cheerio = require('cheerio');
var express = require('express');
var url = require('url');
var mysql = require('mysql');
var async = require('async');

var app = express();
var connection;
var baseUrl = 'https://www.douban.com/group/shanghaizufang/discussion?start=0';
var urls = [];
for(var i = 0; i < 100; i++){

	// note: do more here
	urls.push(baseUrl);
}
console.log('urls',urls);

// 异步抓取
async.mapLimit(urls, 4, function (url, callback){
	getHtml(url, callback);
},function (err, result) {
	console.log(err);
});

// note: 需要传入calback
function getHtml (url, callback) {
	request.get(url).end(function (err, res) {
		if(err){
			return console.log('error ', err);
		}

		analyze(res);
		callback(null, url + ' html content');
	});
}

// @param response html
function analyze (res) {
	var dt = [];
	var $ = cheerio.load(res.text);
	$("#content .article td.title a").each(function(index, ele){
		var href = $(ele).attr('href');
		var title = $(ele).text();
		var date = $(ele).parent().siblings('.time').text();
		var obj = {
			href:href,
			title:title,
			date:date
		};
		dt.push(obj);
	});
	console.log('urls', dt);


	// 查询
	connect (myInsert, dt);
	
}

// mysql connect
function connect (func, dt) {
	connection = mysql.createConnection({
		host:'localhost',
		user:'root',
		password:'123456789',
		database:'node',
		port:'8889'
	});
	connection.connect(function(err){
		if(err){
			console.error('error connecting: ' + err.stack);
			return;
		}
		console.log('connection success');
	});

	func(dt);

	connection.end();
	
}

// insert
function myInsert (dt) {
	// connect();
	for(var i = 0;i < dt.length; i++){
		var query = "insert into douban (href,title,time) values ("+connection.escape(dt[i].href)+","+connection.escape(dt[i].title)+","+connection.escape(dt[i].date)+");";

		connection.query(query, function (error, results, fields) {
		  if (error){
		  	console.log(error);
		  	return;
		  }

		  // console.log(query);
		});
	}

	// connection.end();
}

function myDelete () {

}


function mySelect () {
	var query = 'select * from douban where 1';
	connection.query(query, function (error, results, fields) {
		  if (error){
		  	console.log(error);
		  	return;
		  }

		  console.log('results',results);
		});
}

function myUpdate () {

}








