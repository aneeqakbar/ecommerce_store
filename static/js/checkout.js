const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Create an instance of the Stripe object with your publishable API key
        var stripe = Stripe("{{ STRIPE_PUBLIC_KEY }}");
        var checkoutButton = document.querySelector(".cart_checkout_btn");
        checkoutButton.addEventListener("click", function () {
        fetch("{% url 'shop:create-checkout-session'%}", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (session) {
                // session.id is the fetched checkout_session.id
                return stripe.redirectToCheckout({ sessionId: session.id });
            })
            .then(function (result) {
            // If redirectToCheckout fails due to a browser or network
            // error, you should display the localized error message to your
            // customer using error.message.
            if (result.error) {
                alert(result.error.message);
                }
            })
            .catch(function (error) {
                console.error("Error:", error);
            });
        });