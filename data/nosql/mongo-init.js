db.createUser(
        {
            user: "mongo_user",
            pwd: "mongo_pass",
            roles: [
                {
                    role: "readWrite",
                    db: "mongo_test"
                }
            ]
        }
);

db.customer_details.insert([
    {
        "customer_id": 1,
        "gender": "male",
        "birthday": new ISODate("1988-01-10"),
        "interests": ["woodworking", "grilling", "fitness"],
        "preferences": {
            "notifications": {
                "security_emails": true,
                "informational_emails": true
            },
            "appearance": {
                "font_color": "red",
                "background_color": "blue"
            },
            "backups": {
                "phone": "555-555-5555"
            }
        },
        "customer_complaints": [
            {"date": new ISODate("2022-01-01"), "issue": "package arrived damaged", "order_id": "ord_aaa-aaa"},
            {"date": new ISODate("2022-01-02"), "issue": "order not complete", "order_id": "ord_ccc-ccc"}
        ],
    },
     {
        "customer_id": 2,
        "gender": "female",
        "birthday": new ISODate("1985-03-05"),
        "interests": ["computer science", "welding", "art"],
        "preferences": {
            "notifications": {
                "security_emails": true,
                "informational_emails": false
            },
            "appearance": {
                "font_color": "black",
                "background_color": "white"
            },
            "backups": {
                "phone": "111-111-1111"
            }
        },
        "customer_complaints": [
            {"date": new ISODate("2021-12-31"), "issue": "item not as advertised", "order_id": "ord_bbb-bbb"},
        ],
    },
    {
        "customer_id": 3,
        "gender": "female",
        "birthday": new ISODate("1990-02-28"),
        "interests": ["baking", "art", "hiking"],
          "preferences": {
            "notifications": {
                "security_emails": true,
                "informational_emails": false
            },
            "appearance": {
                "font_color": "black",
                "background_color": "cyan"
            }
        }
    }
]);

db.business_account.insert([
    {
        "members": [1, 3],
        "account_name": "Our Business Account",
        "account_balance": 500.0
    }
])

db.professional_information.insert([
    {
        "customer": {
            "identifier": 1,
            "workplace": "Jane's Restaurant",
            "title": "Head Chef"
        }
    },
    {
        "customer": {
            "identifier": 2,
            "workplace": "Joe's Software Company",
            "title": "Software Engineer"
        }
    }
])

db.customer_feedback.insert([
    {
        "emails": ["customer-1@example.com", "customer-1-alt@example.com"],
        "rating": 3,
        "date": new ISODate("2022-01-05"),
        "message": "Customer service wait times have increased to over an hour."
    },
    {
        "emails": ["customer-2@example.com"],
        "rating": 5,
        "date": new ISODate("2022-01-10"),
        "message": "Customer service rep Virginia was extremely helpful and answered all my questions."
    }
])


db.composite_pk_test.insert([
    {"id_a":1, "id_b":10, "description":"linked to customer 1", "customer_id":"1"},
    {"id_a":1, "id_b":11, "description":"linked to customer 2", "customer_id":"2"},
    {"id_a":2, "id_b":10, "description":"linked to customer 3", "customer_id":"3"}
    ])

//values to support test by specific objectId search

db.type_link_test.insert([
    {"_id":ObjectId("000000000000000000000001"), "name":"v1", "key":1, "email":"test1@example.com"},
    {"_id":ObjectId("000000000000000000000002"), "name":"v2", "key":2, "email":"test1@example.com"},
    {"_id":ObjectId("000000000000000000000003"), "name":"v3", "key":3, "email":"test1@example.com"}
])
