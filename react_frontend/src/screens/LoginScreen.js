import React, { useState, useEffect, useCallback } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { Form, Button, Row, Col } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { login } from "../actions/userActions";
import { googleAuth, githubAuth } from "../actions/authActions";
import Message from "../components/Message";
import Loader from "../components/Loader";

const loginFormStyle = {
  backgroundColor: "#2a2a2a",
  padding: "2rem",
  borderRadius: "10px",
  color: "#fff",
};

function LoginScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const userLogin = useSelector((state) => state.userLogin);
  const auth = useSelector((state) => state.auth);

  const { loading, error, userInfo } = userLogin || {};
  const {
    loading: socialLoading,
    error: socialError,
    userInfo: socialUser,
  } = auth || {};

  // Handle successful login (email or social)
  useEffect(() => {
    const user = userInfo || socialUser;
    if (user && Object.keys(user).length > 0) {
      localStorage.removeItem("tempUserInfo");
      navigate("/");
    }
  }, [userInfo, socialUser, navigate]);

  // ✅ GitHub Login Handler
  const handleGitHubLogin = () => {
    const clientId = process.env.REACT_APP_GITHUB_CLIENT_ID;
    const redirectUri = encodeURIComponent(`${window.location.origin}/login`);
    const githubUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=user:email`;
    window.location.href = githubUrl;
  };

  // ✅ GitHub Callback Handler
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const code = params.get("code");

    if (code) {
      dispatch(githubAuth(code));
    }
  }, [location.search, dispatch]);

  // ✅ Memoized Google Callback
  const handleGoogleCallback = useCallback(
    async (response) => {
      if (response?.credential) {
        try {
          const result = await dispatch(googleAuth(response.credential));
          if (result?.user) {
            localStorage.setItem("userInfo", JSON.stringify(result.user));
            localStorage.setItem("access_token", result.tokens.access);
            localStorage.setItem("refresh_token", result.tokens.refresh);
            dispatch({ type: "USER_LOGIN_SUCCESS", payload: result.user });
            navigate("/");
          }
        } catch (error) {
          console.error("Google auth error:", error);
        }
      }
    },
    [dispatch, navigate]
  );

  // ✅ Google Login Button Initialization
  useEffect(() => {
    if (window.google) {
      window.google.accounts.id.initialize({
        client_id:
          "13550565736-r30nr250r4mdu91rgdlfrjpsrhaeuiu6.apps.googleusercontent.com",
        callback: handleGoogleCallback,
        auto_select: false,
        cancel_on_tap_outside: true,
      });

      window.google.accounts.id.renderButton(
        document.getElementById("google-login-button"),
        {
          theme: "filled_black",
          width: '100%',       
          shape: 'rectangular',
          size: "large",
          text: "continue_with",
        }
      );
    }
  }, [handleGoogleCallback]);

  // Handle form submission
  const submitHandler = (e) => {
    e.preventDefault();
    dispatch(login(email, password));
  };
  // Handle GitHub login

  return (
    <Row className="justify-content-md-center mt-5">
      <Col md={6}>
        <div style={loginFormStyle}>
          <h2 className="text-center mb-4">Sign In</h2>

          {(error || socialError) && (
            <Message variant="danger">{error || socialError}</Message>
          )}

          {(loading || socialLoading) && <Loader />}

          {/* Email/Password Login Form */}
          <Form onSubmit={submitHandler}>
            <Form.Group controlId="email" className="mb-3">
              <Form.Label>Email Address</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="bg-dark text-light"
                required
                disabled={loading || socialLoading}
              />
            </Form.Group>

            <Form.Group controlId="password" className="mb-4">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="bg-dark text-light"
                required
                disabled={loading || socialLoading}
                minLength={6}
              />
            </Form.Group>

            <div className="d-grid gap-2">
              <Button
                type="submit"
                variant="primary"
                className="py-2"
                disabled={loading || socialLoading || !email || !password}
              >
                {loading ? "Signing In..." : "Sign In"}
              </Button>
            </div>
          </Form>

          {/* Social Login Section */}
          <hr className="my-4" />
          <div className="text-center mb-3">Or Sign in with</div>

          <div className="d-grid gap-3">
            <div
              id="google-login-button"
              className="d-flex justify-content-center"
            ></div>

            <Button
              className="w-100 oauth-button d-flex align-items-center justify-content-center"
              onClick={handleGitHubLogin}
              disabled={socialLoading}
            >
              <i className="fab fa-github me-2 fs-5"></i>
              Continue with GitHub
            </Button>
          </div>

          {/* Registration Link */}
          <Row className="py-3">
            <Col className="text-center">
              New Customer?{" "}
              <Link to="/signup" className="text-primary">
                Register here
              </Link>
            </Col>
          </Row>
        </div>
      </Col>
    </Row>
  );
}

export default LoginScreen;
