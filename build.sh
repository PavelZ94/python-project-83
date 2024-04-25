#!/usr/bin/env bash

psql $DATABASE_URL -f database.sql
