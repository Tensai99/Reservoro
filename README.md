<h1 align="center">
  <a href="http://reservoro.tensaiverse.tech:5000">RESERVORO</a>
</h1>


<details open="open">
<summary>Table of Contents</summary>

- [Introduction](#Introduction)
- [Intallation](#Installation)
- [Usage](#rUsage)
- [Contribution](#contribution)
- [Support](#support)
- [License](#license)
- [Acknowledgements](#acknowledgements)

</details>

---

## Introduction

<table>
<tr>
<td>

Reservoro – Your Gateway to Modern Dining in Malawi

In a clamoring culinary scene where comfort and custom join, Reservoro arises as a reference point of development. Express farewell to the problem of calls and in-person reservations - with Reservoro, booking a table at your #1 Malawian eatery is essentially as easy as a couple of snaps. Our natural internet based stage upsets the manner in which benefactors secure their eating experience, offering a consistent and helpful arrangement custom fitted to the necessities of present day burger joints. <a href="https://github.com/Tensai99/Reservoro">Reservoro Github</a> <a href="https://www.linkedin.com/in/innocent-mtingwi">Author Innocent Mtingwi</a>

At Reservoro, we comprehend the significance of overcoming any barrier among custom and innovation. Our main goal is basic yet significant: to improve availability and smooth out the booking system, while protecting the glow and friendliness that characterize Malawi's eating society. With a promise to greatness and a commitment to consumer loyalty, Reservoro welcomes you to leave on an excursion of culinary investigation, where each booking is a consistent encounter created with care.

Key features of **Reservoro**:

- Effortless Online Bookingeal-Time Availability
- Personalized Notifications
- Comprehensive Menus and Services
- Special Promotions and Offers
- Secure Payment Processing
- Feedback and Reviews
- Mobile-Friendly Design

#### Installation

Please follow these steps for Installation:

1. Install dependencies
    *   use: pip install -r requirements.txt
2. Create database **restaurant**
3. Then Database migration
    *   flask db init
    *   Then config alembic.ini file add this code "sqlalchemy.url = mysql://root:root@localhost/restaurant" 
    *   flask db migrate -m "Initial migration"
    *   flask db upgrade

#### Usage

1. Creating an Account:

    *   To begin using Reservoro, you need to create a personalized account. Once your account is created, you'll have access to all of Reservoro's features.

2. Browsing Available Tables:

    *   After logging in to your Reservoro account, you'll be greeted with a list of available restaurants in your area. Browse through the options and select the restaurant you'd like to make a reservation at. Once you've chosen a restaurant, you'll be able to view available tables and time slots.

3. Making a Reservation:

    *   Select your desired table by clicking on the available time slot. Specify the number of people in your party and choose the date and time for your reservation. Additionally, in the "Occasion" field, you can add any special requests or notes for the restaurant, such as dietary restrictions or special arrangements for celebrations.

4. Confirming Your Reservation:

    *   Review the details of your reservation to ensure everything is correct. Once you're satisfied, click on the "Confirm Reservation" button to finalize your booking. You'll receive a confirmation email and SMS or WhatsApp notification shortly afterward, confirming your reservation details.

5. Managing Your Reservations:

    *   You can easily manage your reservations through your Reservoro account. View, modify, or cancel your bookings as needed. If you have any changes or special requests, you can communicate directly with the restaurant through the messaging feature in your reservation.

## Contribution

We welcome contributions from the community! If you'd like to contribute to Reservoro , please follow these guidelines:

1. Fork the repository
2. Create a new branch: git checkout -b feature/your-feature
3. Make your changes and commit them: git commit -m 'Add your feature'
3. Push to the branch: git push origin feature/your-feature
4. Submit a pull request

## Related Projects

Check out these related projects:

- [OpenTable](https://www.opentable.com/)
- [Bookatable](https://www.bookatable.com/)
- [Resy](https://resy.com/)

## License

This project is licensed under the **MIT license**. Feel free to edit and distribute this template as you like.

See [LICENSE](LICENSE) for more information.

Lost and Found Platform
Connecting people with their lost items and fostering a community-driven approach to reuniting valuables through a centralized and user-friendly platform.

─
<TEAM>
Team Member: Innocent Mtingwi
Role: Project Manager and Full Stack Developer
Reasoning:
The chosen role of Project Manager and Full Stack Developer is based on the understanding that a single individual will be responsible for overseeing the entire project lifecycle, from conceptualization to implementation. This streamlined approach ensures quick decision-making, efficient communication, and a seamless integration of both the front-end and back-end components of the Lost and Found Platform. This role combines leadership and technical skills, allowing for a comprehensive and cohesive development process

![Reservoro Screenshot](app/static/img/Reservoro.png)